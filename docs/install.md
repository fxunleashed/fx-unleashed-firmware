# Installing the wheel app patch

Read [firmware-warning.md](firmware-warning.md) first. Do this only when you can sit with the wheel for ten minutes
without interruption, with the wheel on its base, the base powered, and the wheel's USB cable plugged into the PC.

You need: **SimPro Manager 3** installed (it keeps Simagic's original wheel app on your PC), **Windows PowerShell**
(already in Windows) and this repository (download it as a zip from the green *Code* button and unzip it).

## 1. Check your copy and the patch (writes nothing)

Open PowerShell in the folder you unzipped and run:

```
powershell -ExecutionPolicy Bypass -File tools\apply-patch.ps1 -VerifyOnly
```

**You should see:** "Original checks out (Simagic's wheel app 1.3.11 ...)" and "The patch applies cleanly".
**If you see STOPPED:** read the message. The usual reasons are that SimPro Manager 3 isn't installed (the file lives in its
firmware folder: pass `-Stock` with the file's path if yours is elsewhere), that it's a different wheel app version
than 1.3.11, or that the file in SimPro's folder is already modified. Don't go on until this check passes.

## 2. Make the patched file

```
powershell -ExecutionPolicy Bypass -File tools\apply-patch.ps1 -IUnderstandTheRisks
```

Passing `-IUnderstandTheRisks` means you read the warning and accept it for your own wheel. It writes the patched file to
`Documents\FX Unleashed\` and checks its checksum against the patch's. Your original is not touched.

## 3. Install it with SimPro

SimPro installs the file that sits in its own firmware folder, so the patched file goes there for the install and
Simagic's original goes back right after. SimPro's folder is
`%LOCALAPPDATA%\SIMAGIC\Simpro3\firmware\wheel\fx_pro\`.

1. Close SimPro. Copy the original `FXPro_App-V1.3.11.0-00000000.sfu` from that folder somewhere safe (it is the thing
   you put back in step 5).
2. Copy the patched file from `Documents\FX Unleashed\` over the one in SimPro's folder and **name it exactly
   `FXPro_App-V1.3.11.0-00000000.sfu`**.
3. Start SimPro (wheel on USB). Open the FX Pro, Firmware, and **reinstall wheel app 1.3.11**. Don't unplug or power off
   anything until SimPro says it's done.
4. If SimPro hangs after the wheel goes into boot mode: close SimPro, start it again and reinstall; it installs to a
   wheel that's already in boot mode.
5. **Put Simagic's original back right away** (copy it over the file in SimPro's folder) so no later SimPro update can
   flash the patch by accident. Check it: `Get-FileHash` of that file must read
   `16DD09CF2E76D6EE34E2C16D7AA2B6C2F3AE407A2B909298FEE98A46248EB6CF`.

**You should see:** the wheel restarts normally and works as before. In SimHub, the FX Unleashed plugin's Wheel tab
says "patch build 9".

## If something goes wrong

- The wheel doesn't start or looks wrong after the install: install the original ([back-to-stock.md](back-to-stock.md))
  and tell us what you saw.
- SimPro doesn't start at all: that is a separate SimPro launcher problem. Starting
  `C:\Program Files (x86)\SIMAGIC\Simpro3\bin\simpro3.exe` directly worked for us.
- Anything else: open an issue with what you did and saw.
