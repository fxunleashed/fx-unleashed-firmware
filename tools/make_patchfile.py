"""Make a patch file for the FX Unleashed wheel app (maintainers; users apply it with tools/apply-patch.ps1).

    python make_patchfile.py STOCK.sfu PATCHED.sfu --build 9 -o ../patches/build9.fxpatch.json

STOCK.sfu is Simagic's original wheel app file, PATCHED.sfu is our build of it. Both are inputs only: the patch file
holds neither of them. It holds

  * "xor": for the few bytes of the stock file that our change touches, stock byte XOR patched byte (a difference,
    not a copy of either side), and
  * "append": the bytes our change adds after the end of the stock file (our own code, already in the form the wheel
    needs), plus the sizes and SHA-256 checksums of the file it applies to and of the file it makes.

Applying it needs only the user's own stock file: copy it, XOR the differences in, add the appended bytes, check the
checksum. Nothing in a patch file or in these tools can decrypt or make firmware by itself.

The script checks its own work: it applies the patch it just made to the stock file and requires the patched file back,
byte for byte, and it refuses to write a patch file that contains a run of the stock file's own bytes.
"""
import argparse
import hashlib
import json
import os
import sys

FORMAT = 1
STOCK_NAME = "FXPro_App-V1.3.11.0-00000000.sfu"
# Simagic's original wheel app 1.3.11, as SimPro ships it
KNOWN_STOCK_SHA256 = "16dd09cf2e76d6ee34e2c16d7aa2b6c2f3ae407a2b909298fee98a46248eb6cf"
LICENSE = "GPL-3.0-or-later"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def make(stock, patched, build, merge_gap=8):
    """The patch (a dict) that turns `stock` into `patched`."""
    if len(patched) < len(stock):
        raise ValueError("the patched file is shorter than the stock file: not supported")
    runs, start, last = [], None, None
    for i in range(len(stock)):
        if stock[i] == patched[i]:
            continue
        if start is None:
            start = last = i
        elif i - last <= merge_gap:
            last = i
        else:
            runs.append((start, last))
            start = last = i
    if start is not None:
        runs.append((start, last))
    xor = [{"offset": a, "hex": bytes(stock[i] ^ patched[i] for i in range(a, b + 1)).hex()} for a, b in runs]
    return {
        "format": FORMAT,
        "title": f"FX Unleashed wheel app, build {build}",
        "build": build,
        "licence": LICENSE,
        "note": "Differences only: no Simagic file or bytes are in here. Apply with tools/apply-patch.ps1 to your own copy.",
        "source": {"name": STOCK_NAME, "size": len(stock), "sha256": sha(stock)},
        "result": {"size": len(patched), "sha256": sha(patched)},
        "xor": xor,
        "append": bytes(patched[len(stock):]).hex(),
    }


def apply(stock, patch):
    """The patched file, or ValueError. Mirrors tools/apply-patch.ps1."""
    if patch.get("format") != FORMAT:
        raise ValueError("unknown patch format")
    src, res = patch["source"], patch["result"]
    if len(stock) != src["size"] or sha(stock) != src["sha256"]:
        raise ValueError("this is not the file the patch is for")
    out = bytearray(stock)
    for seg in patch["xor"]:
        o, d = seg["offset"], bytes.fromhex(seg["hex"])
        if o < 0 or o + len(d) > len(stock):
            raise ValueError("a change falls outside the file")
        for i, b in enumerate(d):
            out[o + i] ^= b
    out += bytes.fromhex(patch["append"])
    if len(out) != res["size"] or sha(out) != res["sha256"]:
        raise ValueError("the result doesn't match its checksum: nothing to write")
    return bytes(out)


def leaks_stock_bytes(stock, patch, window=12):
    """True if any `window`-byte run of the stock file appears in what the patch carries."""
    windows = {bytes(stock[i:i + window]) for i in range(len(stock) - window + 1)}
    carried = [bytes.fromhex(patch["append"])] + [bytes.fromhex(s["hex"]) for s in patch["xor"]]
    return any(bytes(c[i:i + window]) in windows for c in carried for i in range(len(c) - window + 1))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("stock")
    ap.add_argument("patched")
    ap.add_argument("--build", type=int, required=True)
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--any-stock", action="store_true", help="don't require Simagic's 1.3.11 file as the source")
    a = ap.parse_args(argv)
    stock, patched = open(a.stock, "rb").read(), open(a.patched, "rb").read()
    if not a.any_stock and sha(stock) != KNOWN_STOCK_SHA256:
        print(f"{a.stock} is not the original wheel app 1.3.11 (sha256 {sha(stock)})", file=sys.stderr)
        return 2
    patch = make(stock, patched, a.build)
    if apply(stock, patch) != patched:
        print("self-check failed: applying the patch doesn't give the patched file", file=sys.stderr)
        return 3
    if leaks_stock_bytes(stock, patch):
        print("self-check failed: the patch carries a run of the stock file's own bytes", file=sys.stderr)
        return 4
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(patch, f, indent=1)
        f.write("\n")
    n = sum(len(s["hex"]) // 2 for s in patch["xor"])
    print(f"{a.out}: build {a.build}, {len(patch['xor'])} changes ({n} bytes) + {len(patch['append']) // 2} bytes appended")
    print(f"  applies to {patch['source']['sha256']}")
    print(f"  makes      {patch['result']['sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
