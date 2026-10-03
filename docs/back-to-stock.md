# Back to Simagic's original

You can return to Simagic's own wheel app at any time, with SimPro, the same way you installed the patch.

1. Check that the file in SimPro's folder
   (`%LOCALAPPDATA%\SIMAGIC\Simpro3\firmware\wheel\fx_pro\FXPro_App-V1.3.11.0-00000000.sfu`) is Simagic's original: its
   SHA-256 is `16dd09cf2e76d6ee34e2c16d7aa2b6c2f3ae407a2b909298fee98a46248eb6cf` (`Get-FileHash <file>` in PowerShell).
   If you followed [install.md](install.md) it is, because you put it back. If not, restore the copy of the original
   you kept in step 1 of the install.
2. Wheel on USB, base on. In SimPro: the FX Pro, Firmware, **reinstall wheel app 1.3.11**.
3. Wait until SimPro says it's done. If it hangs after the wheel enters boot mode, close SimPro, start it again and
   reinstall: it installs to a wheel that's already in boot mode.
4. That is Simagic's own firmware again. The plugin's Wheel tab shows no patch build.

Reinstalling firmware always carries a small risk. Don't unplug or power off the wheel while it installs.
