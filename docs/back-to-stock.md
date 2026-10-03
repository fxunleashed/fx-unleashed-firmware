# Back to Simagic's original

You can return to Simagic's own wheel app at any time, with SimPro, the same way you installed ours. (This is the "back to
stock" part of the [full guide](https://fxunleashed.com/start/#updating-and-going-back-to-stock).)

1. **If you turned on the screen's RAM patch (picture memory), turn it off first:** in SimHub open FX Unleashed, then the Wheel
   tab, then the Firmware card, and press **Turn it off**.
2. **Make sure Simagic's original file is in SimPro's folder.** The folder is
   `%LOCALAPPDATA%\SIMAGIC\Simpro3\firmware\wheel\fx_pro` (press Windows key + R, paste it, press Enter) and the file is
   `FXPro_App-V1.3.11.0-00000000.sfu`. If you followed [install.md](install.md) it is there, because you put it back at the end.
   If not, copy the original you saved on your Desktop into that folder and choose **Replace**.
3. **Reinstall in SimPro:** wheel on the base, base on, USB cable in. In SimPro open the FX Pro, Firmware, and **reinstall wheel
   app 1.3.11**.
4. Wait until SimPro says it's done. If it hangs after the wheel enters boot mode, close SimPro, start it again and
   reinstall: it installs to a wheel that's already in boot mode.
5. That is Simagic's own firmware again. The plugin's Wheel tab shows no patch build.

Reinstalling firmware always carries a small risk. Don't unplug or power off the wheel while it installs.

## For the curious

Simagic's original wheel app is 95,232 bytes with SHA-256 `16dd09cf2e76d6ee34e2c16d7aa2b6c2f3ae407a2b909298fee98a46248eb6cf`.
To check the file in SimPro's folder, run `Get-FileHash <file>` in PowerShell and compare.
