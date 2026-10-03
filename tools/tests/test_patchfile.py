"""Tests for make_patchfile.py and apply-patch.ps1 on made-up data (no Simagic file is needed or used).

    python -m unittest discover -s tools/tests -v
"""
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)
import make_patchfile as mp  # noqa: E402


def fake_files(seed=1, size=4096, tail=300):
    rnd = random.Random(seed)
    stock = bytes(rnd.randrange(256) for _ in range(size))
    patched = bytearray(stock)
    for off in (48, 49, 700, 701, 702, 703, 1500, 3000):  # a few separate edits, two of them close together
        patched[off] ^= rnd.randrange(1, 256)
    patched += bytes(rnd.randrange(256) for _ in range(tail))
    return stock, bytes(patched)


class PatchFile(unittest.TestCase):
    def test_round_trip(self):
        stock, patched = fake_files()
        patch = mp.make(stock, patched, build=9)
        self.assertEqual(mp.apply(stock, patch), patched)

    def test_only_changed_bytes_are_carried(self):
        stock, patched = fake_files()
        patch = mp.make(stock, patched, build=9)
        carried = sum(len(s["hex"]) // 2 for s in patch["xor"]) + len(patch["append"]) // 2
        self.assertLess(carried, 400)  # 300 appended + a few edits; nowhere near the 4096 of the file
        self.assertFalse(mp.leaks_stock_bytes(stock, patch))

    def test_the_leak_check_notices_a_copy(self):
        stock, patched = fake_files()
        patch = mp.make(stock, patched, build=9)
        patch["append"] = stock[100:140].hex()
        self.assertTrue(mp.leaks_stock_bytes(stock, patch))

    def test_wrong_stock_is_refused(self):
        stock, patched = fake_files()
        patch = mp.make(stock, patched, build=9)
        other = bytearray(stock)
        other[10] ^= 1
        with self.assertRaises(ValueError):
            mp.apply(bytes(other), patch)

    def test_damaged_patch_is_refused(self):
        stock, patched = fake_files()
        patch = mp.make(stock, patched, build=9)
        h = patch["append"]
        patch["append"] = h[:10] + ("0" if h[10] != "0" else "1") + h[11:]
        with self.assertRaises(ValueError):
            mp.apply(stock, patch)

    def test_change_outside_the_file_is_refused(self):
        stock, patched = fake_files()
        patch = mp.make(stock, patched, build=9)
        patch["xor"][0]["offset"] = len(stock)
        with self.assertRaises(ValueError):
            mp.apply(stock, patch)

    def test_shorter_patched_file_is_not_supported(self):
        stock, patched = fake_files()
        with self.assertRaises(ValueError):
            mp.make(stock, patched[:100], build=9)


@unittest.skipUnless(shutil.which("powershell"), "needs Windows PowerShell")
class PowerShellApplier(unittest.TestCase):
    """tools/apply-patch.ps1 must give exactly what make_patchfile.apply gives, and refuse what it refuses."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.stock, self.patched = fake_files(seed=7)
        self.patch = mp.make(self.stock, self.patched, build=9)
        self.stock_path = os.path.join(self.dir, "stock.sfu")
        self.patch_path = os.path.join(self.dir, "p.json")
        self.out = os.path.join(self.dir, "out.sfu")
        open(self.stock_path, "wb").write(self.stock)
        json.dump(self.patch, open(self.patch_path, "w"))

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def run_ps(self, *extra, stock=None):
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", os.path.join(TOOLS, "apply-patch.ps1"),
               "-Stock", stock or self.stock_path, "-Patch", self.patch_path, "-Out", self.out, *extra]
        return subprocess.run(cmd, capture_output=True, text=True).returncode

    def test_applies_and_matches(self):
        self.assertEqual(self.run_ps("-IUnderstandTheRisks"), 0)
        self.assertEqual(open(self.out, "rb").read(), self.patched)

    def test_verify_only_writes_nothing(self):
        self.assertEqual(self.run_ps("-VerifyOnly"), 0)
        self.assertFalse(os.path.exists(self.out))

    def test_needs_the_acknowledgement(self):
        self.assertEqual(self.run_ps(), 1)
        self.assertFalse(os.path.exists(self.out))

    def test_refuses_another_file(self):
        other = os.path.join(self.dir, "other.sfu")
        b = bytearray(self.stock)
        b[20] ^= 1
        open(other, "wb").write(b)
        self.assertEqual(self.run_ps("-IUnderstandTheRisks", stock=other), 2)
        self.assertFalse(os.path.exists(self.out))

    def test_refuses_an_already_patched_file(self):
        done = os.path.join(self.dir, "done.sfu")
        open(done, "wb").write(self.patched)
        self.assertEqual(self.run_ps("-IUnderstandTheRisks", stock=done), 3)

    def test_never_overwrites_the_original(self):
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", os.path.join(TOOLS, "apply-patch.ps1"),
               "-Stock", self.stock_path, "-Patch", self.patch_path, "-Out", self.stock_path, "-IUnderstandTheRisks"]
        self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
        self.assertEqual(open(self.stock_path, "rb").read(), self.stock)


if __name__ == "__main__":
    unittest.main()
