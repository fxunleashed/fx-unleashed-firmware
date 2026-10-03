# Installing the wheel app

Read [firmware-warning.md](firmware-warning.md) first. Do this only when you can sit with the wheel for ten minutes
without interruption, with the wheel on its base, the base powered, and the wheel's USB cable plugged into the PC.

You need: **SimPro Manager 3** installed (it keeps Simagic's original wheel app on your PC and does the installing) and
**Windows PowerShell** (already in Windows).

## 1. Get the file (two ways, same result)

SimPro's firmware folder is `%LOCALAPPDATA%\SIMAGIC\Simpro3\firmware\wheel\fx_pro\`. In it,
`FXPro_App-V1.3.11.0-00000000.sfu` is Simagic's original wheel app. **First copy it somewhere safe**: you put it back at the
end, and it's your way back to stock. Its SHA-256 should read
`16DD09CF2E76D6EE34E2C16D7AA2B6C2F3AE407A2B909298FEE98A46248EB6CF` (`Get-FileHash <file>` in PowerShell).

**A. Download it.** Take `FXUnleashed-wheelapp-build9.sfu` from the
[Releases](https://github.com/fxunleashed/fx-unleashed-firmware/releases) page and check it:

```
Get-FileHash .\FXUnleashed-wheelapp-build9.sfu
```

The SHA-256 must be exactly `85E7110BA368495120C7E84D210C194D5E9EEC9EACEB3F8F7C148F020FE0F458`, and the size 96,272 bytes. If
it isn't, don't use it.

**B. Make it from your own copy.** Download this repository as a zip (green *Code* button) and unzip it. In its folder:

```
powershell -ExecutionPolicy Bypass -File tools\apply-patch.ps1 -VerifyOnly
```

**You should see:** "Original checks out (Simagic's wheel app 1.3.11 ...)" and "The patch applies cleanly". If you see STOPPED:
read the message (SimPro not installed, a different wheel app version than 1.3.11, or the file in SimPro's folder is already
modified) and don't go on until it passes. Then:

```
powershell -ExecutionPolicy Bypass -File tools\apply-patch.ps1 -IUnderstandTheRisks
```

Passing `-IUnderstandTheRisks` means you read the warning and accept it for your own wheel. It writes the file to
`Documents\FX Unleashed\` and checks its checksum against the patch's. Your original is not touched. The file it writes is
byte for byte the one in way A.

## 2. Install it with SimPro

SimPro installs the file that sits in its own firmware folder, so the new file goes there for the install and Simagic's
original goes back right after.

1. Close SimPro. Make sure you copied the original `FXPro_App-V1.3.11.0-00000000.sfu` somewhere safe (step 1).
2. Copy the new file over the one in SimPro's folder and **name it exactly `FXPro_App-V1.3.11.0-00000000.sfu`**.
3. Start SimPro (wheel on USB). Open the FX Pro, Firmware, and **reinstall wheel app 1.3.11**. Don't unplug or power off
   anything until SimPro says it's done.
4. If SimPro hangs after the wheel goes into boot mode: close SimPro, start it again and reinstall; it installs to a
   wheel that's already in boot mode.
5. **Put Simagic's original back right away** (copy it over the file in SimPro's folder) so no later SimPro update can
   flash the modified one by accident. Check it: `Get-FileHash` of that file must read
   `16DD09CF2E76D6EE34E2C16D7AA2B6C2F3AE407A2B909298FEE98A46248EB6CF`.

**You should see:** the wheel restarts normally and works as before. In SimHub, the FX Unleashed plugin's Wheel tab says
"patch build 9".

## If something goes wrong

- The wheel doesn't start or looks wrong after the install: install the original ([back-to-stock.md](back-to-stock.md))
  and tell us what you saw.
- SimPro doesn't start at all: that is a separate SimPro launcher problem. Starting
  `C:\Program Files (x86)\SIMAGIC\Simpro3\bin\simpro3.exe` directly worked for us.
- Anything else: open an issue with what you did and saw.
