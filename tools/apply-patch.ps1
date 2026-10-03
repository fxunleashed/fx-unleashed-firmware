<#
.SYNOPSIS
  Applies an FX Unleashed custom firmware patch to YOUR OWN copy of Simagic's FX Pro firmware and writes the result next to
  nothing else: it never changes SimPro's files and never overwrites the original.

.DESCRIPTION
  A patch file holds only differences (see tools/make_patchfile.py), never Simagic's firmware. This script:
    1. reads your copy of the original firmware (SimPro keeps it in %LOCALAPPDATA%\SIMAGIC\Simpro3\firmware\wheel\fx_pro)
    2. checks it is Simagic's original 1.3.11 (size and SHA-256). If it isn't, it stops.
    3. applies the differences in memory and checks the result against the checksum in the patch. If it differs, it stops.
    4. only then, and only if you passed -IUnderstandTheRisks, writes the patched file to a NEW place.
  Installing that file on the wheel is a separate step you do yourself in SimPro: see docs/install.md.
  Read docs/firmware-warning.md first. This changes the wheel's own program. It is at your own risk.

.EXAMPLE
  .\apply-patch.ps1 -VerifyOnly                       # check your copy and the patch, write nothing
  .\apply-patch.ps1 -IUnderstandTheRisks              # make the patched file in Documents\FX Unleashed
#>
[CmdletBinding()]
param(
    [string]$Patch,
    [string]$Stock = (Join-Path $env:LOCALAPPDATA "SIMAGIC\Simpro3\firmware\wheel\fx_pro\FXPro_App-V1.3.11.0-00000000.sfu"),
    [string]$Out,
    [switch]$VerifyOnly,
    [switch]$IUnderstandTheRisks
)
$ErrorActionPreference = "Stop"

# (the default can't be written in the parameter block: $PSScriptRoot is empty there in Windows PowerShell 5.1)
if (-not $Patch) { $Patch = Join-Path (Split-Path -Parent $PSScriptRoot) "patches\build9.fxpatch.json" }

function Fail([string]$message, [int]$code = 1) { Write-Host ""; Write-Host "STOPPED: $message" -ForegroundColor Red; exit $code }

function Get-Sha256([byte[]]$bytes) {
    $h = [System.Security.Cryptography.SHA256]::Create()
    try { return (($h.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) -join "") } finally { $h.Dispose() }
}

function ConvertFrom-Hex([string]$hex) {
    $b = New-Object byte[] ($hex.Length / 2)
    for ($i = 0; $i -lt $b.Length; $i++) { $b[$i] = [Convert]::ToByte($hex.Substring(2 * $i, 2), 16) }
    return , $b
}

if (-not (Test-Path -LiteralPath $Patch)) { Fail "the patch file isn't there: $Patch" }
if (-not (Test-Path -LiteralPath $Stock)) { Fail "your copy of the original firmware isn't there: $Stock`nInstall SimPro Manager 3 and let it download the FX Pro firmware, or pass -Stock with the file's path." }

$p = [System.IO.File]::ReadAllText($Patch) | ConvertFrom-Json
if ($p.format -ne 1) { Fail "this patch file has a format ($($p.format)) this script doesn't know. Get a newer copy of the tools." }

Write-Host "Patch   : $($p.title)"
Write-Host "Original: $Stock"

# 1-2. is this Simagic's original?
[byte[]]$stockBytes = [System.IO.File]::ReadAllBytes($Stock)
$stockHash = Get-Sha256 $stockBytes
if ($stockBytes.Length -eq $p.result.size -and $stockHash -eq $p.result.sha256) {
    Fail "this file already IS the custom firmware (checksum $stockHash). Put Simagic's original back first (copy your saved original into SimPro's folder), then run this again." 3
}
if ($stockBytes.Length -ne $p.source.size -or $stockHash -ne $p.source.sha256) {
    Fail ("this is not Simagic's original firmware 1.3.11.`n  expected: $($p.source.size) bytes, sha256 $($p.source.sha256)`n  found   : $($stockBytes.Length) bytes, sha256 $stockHash" +
          "`nIt may be a different version, or already modified. Nothing was changed.") 2
}
Write-Host "Original checks out (Simagic's firmware 1.3.11, sha256 $stockHash)." -ForegroundColor Green

# 3. apply in memory, check the result
[byte[]]$append = ConvertFrom-Hex $p.append
[byte[]]$result = New-Object byte[] ($stockBytes.Length + $append.Length)
[Array]::Copy($stockBytes, $result, $stockBytes.Length)
foreach ($seg in $p.xor) {
    [byte[]]$d = ConvertFrom-Hex $seg.hex
    if ($seg.offset -lt 0 -or ($seg.offset + $d.Length) -gt $stockBytes.Length) { Fail "the patch has a change outside the file. Don't use it." 4 }
    for ($i = 0; $i -lt $d.Length; $i++) { $result[$seg.offset + $i] = $result[$seg.offset + $i] -bxor $d[$i] }
}
[Array]::Copy($append, 0, $result, $stockBytes.Length, $append.Length)
$resultHash = Get-Sha256 $result
if ($result.Length -ne $p.result.size -or $resultHash -ne $p.result.sha256) {
    Fail "the result doesn't match the checksum in the patch (got $resultHash). The patch file may be damaged or changed. Nothing was written." 4
}
Write-Host "The patch applies cleanly: $($result.Length) bytes, sha256 $resultHash." -ForegroundColor Green

if ($VerifyOnly) { Write-Host "`n-VerifyOnly: nothing written."; exit 0 }

# 4. the acknowledgement, then write
if (-not $IUnderstandTheRisks) {
    Write-Host ""
    Write-Host "Before this writes the patched file, read docs/firmware-warning.md. In short:" -ForegroundColor Yellow
    Write-Host "  - Modified firmware isn't made, tested or supported by Simagic, and may void your warranty."
    Write-Host "  - A bug, an interrupted install or a hardware difference could stop the wheel working, rarely beyond what you can recover yourself."
    Write-Host "  - It only changes the wheel's own app (lights, screen, buttons, USB), never the base or force feedback."
    Write-Host "  - You can go back to Simagic's original with SimPro at any time (docs/back-to-stock.md)."
    Write-Host "  - Never unplug or power off the wheel while it installs."
    Write-Host ""
    Write-Host "If you understand and accept this for your own wheel, run it again with -IUnderstandTheRisks." -ForegroundColor Yellow
    exit 1
}

if (-not $Out) {
    $dir = Join-Path ([Environment]::GetFolderPath("MyDocuments")) "FX Unleashed"
    $Out = Join-Path $dir ("FXPro_App-V1.3.11.0-00000000.build" + $p.build + ".sfu")
}
$outFull = [System.IO.Path]::GetFullPath($Out)
if ($outFull -eq [System.IO.Path]::GetFullPath($Stock)) { Fail "the output would overwrite your original. Choose another -Out." }
New-Item -ItemType Directory -Force -Path ([System.IO.Path]::GetDirectoryName($outFull)) | Out-Null
[System.IO.File]::WriteAllBytes($outFull, $result)
$check = Get-Sha256 ([System.IO.File]::ReadAllBytes($outFull))
if ($check -ne $p.result.sha256) { Remove-Item -LiteralPath $outFull -Force; Fail "the file written doesn't match what was made (disk problem?). It was deleted." 4 }

Write-Host ""
Write-Host "Written: $outFull" -ForegroundColor Green
Write-Host "         sha256 $check (it matches the patch)"
Write-Host ""
Write-Host "Next (docs/install.md has the same with more care):"
Write-Host "  1. Close SimPro. Keep a copy of the original: $Stock"
Write-Host "  2. Rename the written file to FXPro_App-V1.3.11.0-00000000.sfu and copy it over the one in SimPro's folder."
Write-Host "  3. Start SimPro, wheel on the base: Settings > Update > Manual Firmware Flash, press Flash on the FX PRO row and select that file. Don't unplug anything until it says it's done."
Write-Host "  4. Put the ORIGINAL back in SimPro's folder straight away and check its sha256 is $($p.source.sha256)."
Write-Host "  5. In SimHub's FX Unleashed plugin, the Wheel tab should show build $($p.build) for the custom firmware."
exit 0
