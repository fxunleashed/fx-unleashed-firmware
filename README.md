# FX Unleashed: wheel app patch for the Simagic FX Pro

> **FX Unleashed is an independent community project.** It is not affiliated with, endorsed by or supported by
> Simagic. Simagic and FX Pro are trademarks of their owner, used only to say which hardware this works with. The
> software is provided "as is", without warranty of any kind. Use it at your own risk.

Unleashed mode of the [FX Unleashed SimHub plugin](https://github.com/fxunleashed/fx-unleashed) needs a modified
version of the FX Pro's own wheel app (lights, screen, buttons, USB). This repository holds that change, packaged so
that **nothing of Simagic's is in it**.

**Read [docs/firmware-warning.md](docs/firmware-warning.md) before you do anything here.** You change your wheel's own
program. It is at your own risk, and going back to Simagic's original is always possible
([docs/back-to-stock.md](docs/back-to-stock.md)).

## What is here, and what is not

| Here | |
|---|---|
| `patches/build9.fxpatch.json` | The change: a few bytes of differences and about 1 KB of our own code, with the checksums of the file it applies to and of the file it makes. |
| `tools/apply-patch.ps1` | Applies the patch to **your own copy** of Simagic's wheel app (the one in SimPro's firmware folder), checks everything, and writes the patched file somewhere new. Never changes SimPro's files. |
| `tools/make_patchfile.py` | How a patch file is made (maintainers). Checks its own work and that no stock bytes leak into the patch. |
| `docs/` | The guide, going back to stock, what each build changes, how it was checked. |

**Not here, and never will be:** Simagic's firmware (original or patched), the key that protects it, or anything
decrypted from it. A patch file cannot make firmware by itself and the tools cannot decrypt anything.

## In short

1. Have SimPro Manager 3 installed: Simagic's original wheel app sits in its firmware folder (`%LOCALAPPDATA%\SIMAGIC\Simpro3\firmware\wheel\fx_pro\`).
2. `powershell -ExecutionPolicy Bypass -File tools\apply-patch.ps1 -VerifyOnly` checks your copy and the patch and writes nothing.
3. Follow [docs/install.md](docs/install.md): the same command with `-IUnderstandTheRisks` writes the patched file, and the guide walks through installing it with SimPro and putting Simagic's original back.

## Builds

The patch is **build 9** and includes builds 4 to 8. What each does: [docs/builds.md](docs/builds.md). How it was
checked: [docs/verification.md](docs/verification.md).

## Licence

[GPL-3.0](LICENSE): no warranty, no liability (sections 15 and 16). See [NOTICE](NOTICE). Issues and questions:
[fx-unleashed issues](https://github.com/fxunleashed/fx-unleashed/issues). If something here shouldn't be public,
please say so there or through GitHub's private reporting on that repository.
