# Installing the custom firmware

**Please read [firmware-warning.md](firmware-warning.md) first.** This changes your wheel's own program, so it is at your own
risk, and Simagic's original is always one flash away.

Do it when you have ten quiet minutes, with the wheel on its base, the base on, and the wheel's USB cable plugged into the PC.
You need **SimPro Manager 3**: it does the flashing.

The same steps are on the website, next to the rest of the setup: [fxunleashed.com/start](https://fxunleashed.com/start/#1-install-the-custom-firmware).

## The steps

1. **Download the custom firmware:** [the latest release](https://github.com/fxunleashed/fx-unleashed-firmware/releases/latest). It is one
   small file ending in `.sfu`.
2. **Close SimPro** completely (also from its icon by the clock).
3. **Open SimPro's firmware folder.** Press the **Windows key + R**, paste
   `%LOCALAPPDATA%\SIMAGIC\Simpro3\firmware\wheel\fx_pro` and press Enter. A folder opens with one file in it,
   `FXPro_App-V1.3.11.0-00000000.sfu`. That is Simagic's original firmware.
4. **Keep Simagic's original:** copy that file to your Desktop. It is your way back.
5. **Swap in ours:** rename the file you downloaded to exactly `FXPro_App-V1.3.11.0-00000000.sfu` (right-click it, Rename), drag
   it into the open folder and choose **Replace the file in the destination**. (If your file names show no `.sfu` ending, leave
   it off when you type the name.)
6. **Flash it with SimPro:** start SimPro and open **Settings > Update**. Scroll to the bottom, to **Manual Firmware Flash**. On
   the **FX PRO** row press **Flash**, then select `FXPro_App-V1.3.11.0-00000000.sfu` in the folder from step 3 (paste that
   folder path into the window's address bar to get there). Wait until SimPro says it's done, and don't unplug or switch anything
   off meanwhile. (If it sits at 0% after the wheel goes into boot mode, close SimPro, open it again and flash again.)
7. **Put Simagic's original back:** copy the file from your Desktop into the same folder and choose **Replace**. Then SimPro's own
   copy is Simagic's again, and a later SimPro update can't flash ours by accident.

**You should see:** the wheel restarts and works as before. In SimHub, the FX Unleashed plugin's Wheel tab shows a build number
for the custom firmware.

## The whole path

The custom firmware is step 1 of 4, and one guide walks you through all of them, start to finish:
[fxunleashed.com/start](https://fxunleashed.com/start/).

1. **Custom firmware:** this page.
2. [**The plugin**](https://fxunleashed.com/start/#2-install-the-plugin): the SimHub plugin that drives the wheel.
3. [**The screen's RAM patch**](https://fxunleashed.com/start/#3-turn-on-picture-memory) (picture memory): optional, but highly
   recommended, because dashes then appear at once and in full colour. The plugin installs it for you and walks you through it.
4. [**Your dashes and lights**](https://fxunleashed.com/start/#4-pick-your-dashes-and-lights): the library, the designer, and sharing.

## If something goes wrong

- The wheel doesn't start or looks wrong after the flash: flash Simagic's original again
  ([back-to-stock.md](back-to-stock.md)) and tell us what you saw.
- SimPro doesn't start at all: that is a separate SimPro launcher problem. Starting
  `C:\Program Files (x86)\SIMAGIC\Simpro3\bin\simpro3.exe` directly worked for us.
- Anything else: ask in the [Discord](https://discord.gg/P9Rz6fXrRc), or [open an issue](https://github.com/fxunleashed/fx-unleashed/issues) with what you did and saw.

---

## For the curious

None of this is needed to install it.

### Check your download

Each release shows the file's SHA-256 fingerprint and size (also in `SHA256SUMS.txt`). In PowerShell, in the folder with the file:

```
Get-FileHash .\FXUnleashed-firmware-build9.sfu
```

The result must match exactly. If it doesn't, don't use the file. Simagic's original in SimPro's folder should read
`16DD09CF2E76D6EE34E2C16D7AA2B6C2F3AE407A2B909298FEE98A46248EB6CF`; check it the same way if you want to be sure you saved the
right one.

### Make the file yourself instead of downloading it

Rather not download a modified vendor file? The patch tool makes the identical file from **your own copy** of Simagic's original.
Download this repository as a zip (green *Code* button) and unzip it. In its folder, in PowerShell:

```
powershell -ExecutionPolicy Bypass -File tools\apply-patch.ps1 -VerifyOnly
```

**You should see:** "Original checks out (Simagic's firmware 1.3.11 ...)" and "The patch applies cleanly". If you see STOPPED, read
the message (SimPro not installed, a different firmware version than 1.3.11, or the file in SimPro's folder is already modified)
and don't go on until it passes. Then:

```
powershell -ExecutionPolicy Bypass -File tools\apply-patch.ps1 -IUnderstandTheRisks
```

Passing `-IUnderstandTheRisks` means you read the warning and accept it for your own wheel. It writes the file to
`Documents\FX Unleashed\` and checks its checksum against the patch's. Your original is not touched. The file it writes is byte for
byte the release file; use it in step 5 above in place of the download.
