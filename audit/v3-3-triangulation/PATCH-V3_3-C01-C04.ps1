Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Repair pass: remove literal escape artifacts and replacement characters left by the prior patch transport.
$Source = Join-Path (Get-Location) 'audit\v3-3-triangulation\source\download_ticks_v3_3.ps1'
$ExpectedBlob = '3af21d0e77a496530eb5e4d7a706c7aa448b3377'

if (-not (Test-Path -LiteralPath $Source)) { throw "Source absent: $Source" }
$ActualBlob = (git hash-object $Source).Trim()
if ($ActualBlob -ne $ExpectedBlob) { throw "Unexpected source blob. Expected=$ExpectedBlob Actual=$ActualBlob" }

$Text = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($Source))
$LiteralBacktickN = [string][char]96 + 'n'
if ($Text.Contains($LiteralBacktickN)) {
    $Text = $Text.Replace($LiteralBacktickN, [Environment]::NewLine)
}

$Text = $Text.Replace('Chronologie d�croissante', 'Chronologie decroissante')
$Text = $Text.Replace('RAW pr�sent mais diff�rent de la preuve VALID persist�e.', 'RAW present mais different de la preuve VALID persistee.')
$Text = $Text.Replace('d�j� VALID et hash v�rifi�', 'deja VALID et hash verifie')

if ($Text.Contains($LiteralBacktickN)) { throw 'LITERAL_BACKTICK_N_REMAINS' }
if ($Text.Contains([char]0xFFFD)) { throw 'UTF8_REPLACEMENT_CHARACTER_REMAINS' }
if ($Text -match 'Ã.') { throw 'M02_MOJIBAKE_REMAINS' }

[IO.File]::WriteAllText($Source, $Text, (New-Object Text.UTF8Encoding($false)))

$NewBlob = (git hash-object $Source).Trim()
if ($NewBlob -eq $ExpectedBlob) { throw 'Patch produced no source change.' }

$Errors = $null
[void][System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path $Source), [ref]$null, [ref]$Errors)
if ($null -ne $Errors -and $Errors.Count -gt 0) { throw "PowerShell parser errors: $($Errors.Count)" }

$Checks = [ordered]@{
    C01 = $Text.Contains('if ($Timestamp -lt $PreviousTimestamp)') -and -not $Text.Contains('if ($Timestamp -le $PreviousTimestamp)')
    C02 = $Text.Contains('SKIP_RAW_HASH_MISMATCH') -and $Text.Contains('Get-FileHash -LiteralPath $RawPath -Algorithm SHA256')
    C03 = $Text.Contains('EMPTY_DOWNLOAD: dukascopy-node returned exit 0 but produced no CSV')
    C04 = $Text.Contains('RAW_REMOVED')
    H03 = $Text.Contains('NODE_RUNTIME_UNAVAILABLE')
    M01 = -not $Text.Contains('$Matches = @(')
    M02 = -not $Text.Contains([char]0xFFFD) -and -not ($Text -match 'Ã.')
    M03 = $Text.Contains('[IO.Path]::GetTempPath()')
}
$Checks.GetEnumerator() | ForEach-Object { Write-Host "$($_.Key)=$($_.Value)" }
if ($Checks.Values -contains $false) { throw 'STATIC_PATCH_ASSERTION_FAILED' }

Write-Host 'V3.3 ENCODING/ESCAPE CORRECTION = PASS'
Write-Host "OLD_BLOB=$ExpectedBlob"
Write-Host "NEW_BLOB=$NewBlob"
Write-Host 'RUNTIME QUALIFICATION REMAINS BLOCKED UNTIL AUTONOMOUS HARNESS EXECUTION.'