# What each build changes

The patch file is **build 9**; each build includes the ones before it. Everything waits for the plugin to switch it on
(a value it writes into the wheel's memory, which is random at power-on), so a wheel with the patch but without the
plugin behaves as stock, with one exception: build 6's restart into USB mode (below).

| Build | What it adds |
|---|---|
| 4 | Every one of the 38 lights takes its colour from the PC; the PC can own the screen and gives it back when it stops. |
| 5 | The dash button is sent to the PC as a controller button in USB mode instead of switching the wheel's own pages. |
| 6 | A wheel that started on the base restarts into USB mode when a PC is on its cable (at most three times per power-on). |
| 7 | The wheel tells the plugin which build it runs. |
| 8 | The dash button and the two upper paddles are sent to buttons you choose (on a stock wheel the upper paddles send nothing over USB). |
| 9 | The wheel reports 48 buttons instead of 40, so the dash button and upper paddles get their own slots (41 to 43) and share nothing with an encoder or a roller. SimPro still connects and reads the wheel as before. |

It changes only the wheel's own app. The bootloader, the flag page and the firmware update path are never touched, and
your base and force feedback aren't involved. [verification.md](verification.md) says how every build is checked.
