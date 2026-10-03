# FX Unleashed: wheel app for the Simagic FX Pro

> **FX Unleashed is an independent community project.** It is not affiliated with, endorsed by or supported by
> Simagic. Simagic and FX Pro are trademarks of their owner, used only to say which hardware this works with. The
> software is provided "as is", without warranty of any kind. Use it at your own risk.

Unleashed mode of the [FX Unleashed SimHub plugin](https://github.com/fxunleashed/fx-unleashed) needs a modified
version of the FX Pro's own wheel app (lights, screen, buttons, USB). This repository publishes it.

**Read [docs/firmware-warning.md](docs/firmware-warning.md) before you do anything here.** You change your wheel's own
program. It is at your own risk, and going back to Simagic's original is always possible
([docs/back-to-stock.md](docs/back-to-stock.md)).

## Get it

**[Download the newest wheel app](https://github.com/fxunleashed/fx-unleashed-firmware/releases/latest)**: one small file,
`FXUnleashed-wheelapp-build9.sfu` (build 9, which includes builds 4 to 8). Then follow the simple steps in
[docs/install.md](docs/install.md). The full guide, which goes on with the plugin and the screen's RAM patch (picture memory, optional but
highly recommended), is at [fxunleashed.com/start](https://fxunleashed.com/start/).
**It is Simagic's wheel app 1.3.11 with our changes**, so it is Simagic's software, not covered by our licence, and shared without
Simagic's involvement. It may be removed at any time.

| For the curious | |
|---|---|
| The file's fingerprint | 96,272 bytes, SHA-256 `85e7110ba368495120c7e84d210c194d5e9eec9eaceb3f8f7c148f020fe0f458` (also on each release and in `SHA256SUMS.txt`). |
| `patches/build9.fxpatch.json` + `tools/apply-patch.ps1` | The same file, made on your PC from **your own copy** of Simagic's wheel app (the one in SimPro's firmware folder), byte for byte. For those who'd rather not download a modified vendor file. The patch holds only our changes: a few bytes of differences and about 1 KB of our own code. |

## What is here, and what is not

| Here | |
|---|---|
| The release | Build 9 of the wheel app, with its checksum. |
| `patches/` and `tools/` | The patch file and the tool that applies it (`apply-patch.ps1`), and how a patch file is made (`make_patchfile.py`) with its tests. |
| `docs/` | The guide, going back to stock, what each build changes, how it was checked. |

**Not here, and never will be:** the key that protects Simagic's firmware, any tool that decrypts it, anything decrypted
from it, or Simagic's original files. The firmware can be installed without any of that.

## Builds

Build 9 includes builds 4 to 8. What each does: [docs/builds.md](docs/builds.md). How it was checked:
[docs/verification.md](docs/verification.md).

## Licence

Our code (the tools, the patch file, the documentation) is [GPL-3.0](LICENSE): no warranty, no liability (sections 15 and
16). The release file is Simagic's software with our changes and is **not** covered by it. See [NOTICE](NOTICE). Issues and
questions: [fx-unleashed issues](https://github.com/fxunleashed/fx-unleashed/issues). If something here shouldn't be public,
please say so there or through GitHub's private reporting on that repository.
