# How it is checked

**The release file.** `FXUnleashed-firmware-build9.sfu` is exactly the file the patch below makes (same size, same SHA-256), so downloading it
and making it from your own copy give the same bytes.

**What the patch file makes.** Applying `patches/build9.fxpatch.json` to Simagic's original firmware (SHA-256
`16dd09cf...b6cf`, 95,232 bytes) gives a file of 96,272 bytes with SHA-256
`85e7110ba368495120c7e84d210c194d5e9eec9eaceb3f8f7c148f020fe0f458`. That is byte for byte the file that has been running
on the maintainer's FX Pro (installed through SimPro, read back as build 9). Nothing is rebuilt on your PC: you
get exactly that file or the tool stops.

**The tools check themselves.** `tools/apply-patch.ps1` refuses unless your file is Simagic's original (size and
checksum), unless the result matches the patch's checksum, and unless you passed `-IUnderstandTheRisks`; it never
overwrites the original and deletes its output if it can't read it back correctly. `tools/make_patchfile.py` applies
the patch it just made and requires the patched file back, and refuses a patch that carries any run of the original
file's own bytes. `python -m unittest discover -s tools/tests` runs both tools on made-up data, including every refusal.

**Before a build was ever installed**, each changed routine was run in an emulator, from both the original and the
patched image, over every input and mode, with a negative control that has to fail; the package was unpacked again and
compared byte for byte; and each build changed one thing so a problem on a wheel points at one change. Then it was
installed on the maintainer's wheel and used.

**What is not checked:** every wheel, base, revision and setup. We tested on one FX Pro on an Alpha EVO base.
