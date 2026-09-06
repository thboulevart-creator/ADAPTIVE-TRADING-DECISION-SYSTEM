Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Repo = (Get-Location).Path
$Source = Join-Path $Repo 'audit\v3-3-triangulation\source\download_ticks_v3_3.ps1'
$ExpectedOldBlob = '3dc826146c527d7e2d1d51c4879b2b61c1c01dd7'

if (-not (Test-Path -LiteralPath $Source)) { throw "Source absent: $Source" }
$Text = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($Source))
$ActualBlob = (git hash-object $Source).Trim()
if ($ActualBlob -ne $ExpectedOldBlob) { throw "Unexpected source blob. Expected=$ExpectedOldBlob Actual=$ActualBlob" }
$Backup = "$Source.bak_before_C01_C04_$(Get-Date -Format yyyyMMdd_HHmmss)"
Copy-Item -LiteralPath $Source -Destination $Backup -Force

# C01
if (-not $Text.Contains('if ($Timestamp -le $PreviousTimestamp)')) { throw 'C01 original guard not found' }
$Text = $Text.Replace('if ($Timestamp -le $PreviousTimestamp) {','if ($Timestamp -lt $PreviousTimestamp) {')
$Text = $Text.Replace('Chronologie non strictement croissante','Chronologie décroissante')

# M01
$Text = $Text.Replace('$Matches = @(','$MatchingRecords = @(')
$Text = $Text.Replace('$Matches.Count','$MatchingRecords.Count')
$Text = $Text.Replace('return $Matches[-1]','return $MatchingRecords[-1]')

# M03
$TempPattern = '(?ms)\$TempRoot\s*=\s*Join-Path\s+`\s*\$env:TEMP\s+`\s*\("dukascopy_v3_3_" \+ \$RunId \+ "_" \+ \$DateString\)'
$TempReplacement = '$TempBase = if ([string]::IsNullOrWhiteSpace($env:TEMP)) { [IO.Path]::GetTempPath() } else { $env:TEMP }`n    $TempRoot = Join-Path `n        $TempBase `n        ("dukascopy_v3_3_" + $RunId + "_" + $DateString)'
if (-not [regex]::IsMatch($Text,$TempPattern)) { throw 'M03 original temp block not found' }
$Text = [regex]::Replace($Text,$TempPattern,$TempReplacement,1)

# C02
$SkipPattern = '(?ms)(\s*)Write-Log "\$DateString \| SKIP \| déjà VALID".*?\s*return "SKIP"'
$SkipReplacement = @'
$1if ([string]::IsNullOrWhiteSpace([string]$LatestValid.sha256) -or [string]::IsNullOrWhiteSpace([string]$LatestValid.file_size_bytes)) {
$1    Add-ManifestRecord -Date $Date -Status "BLOCKED" -File $RawPath -Validation "VALID_PROOF_INCOMPLETE" -ErrorMessage "Le record VALID ne contient pas une preuve SHA-256/taille exploitable."
$1    return "BLOCKED"
$1}
$1$CurrentRawInfo = Get-Item -LiteralPath $RawPath
$1$CurrentRawHash = (Get-FileHash -LiteralPath $RawPath -Algorithm SHA256).Hash
$1if ([int64]$CurrentRawInfo.Length -ne [int64]$LatestValid.file_size_bytes -or $CurrentRawHash -ne [string]$LatestValid.sha256) {
$1    Add-ManifestRecord -Date $Date -Status "INTEGRITY_FAILURE" -File $RawPath -FileSizeBytes $CurrentRawInfo.Length -Sha256 $CurrentRawHash -Validation "SKIP_RAW_HASH_MISMATCH" -ErrorMessage "RAW présent mais différent de la preuve VALID persistée."
$1    Write-Log "$DateString | INTEGRITY_FAILURE | SKIP_RAW_HASH_MISMATCH"
$1    return "INTEGRITY_FAILURE"
$1}
$1Write-Log "$DateString | SKIP | déjà VALID et hash vérifié"
$1Add-ManifestRecord -Date $Date -Status "SKIP" -File $RawPath -FileSizeBytes $CurrentRawInfo.Length -TickCount $LatestValid.tick_count -Sha256 $CurrentRawHash -FirstTimestamp $LatestValid.first_timestamp -LastTimestamp $LatestValid.last_timestamp -Validation "ALREADY_VALID_HASH_VERIFIED"
$1return "SKIP"
'@
if (-not [regex]::IsMatch($Text,$SkipPattern)) { throw 'C02 original SKIP block not found' }
$Text = [regex]::Replace($Text,$SkipPattern,$SkipReplacement,1)

# C04
$PostPattern = '(?ms)(\$PostValidation\.Status -ne "VALID"\).*?Write-Log \(\s*"\$DateString \| INTEGRITY_FAILURE \| " \+\s*"post-copy validation"\s*\)\s*)(return "INTEGRITY_FAILURE")'
if (-not [regex]::IsMatch($Text,$PostPattern)) { throw 'C04 post-copy block not found' }
$Text = [regex]::Replace($Text,$PostPattern,'$1Remove-Item -LiteralPath $RawPath -Force -ErrorAction Stop`n`n            Write-Log "$DateString | INTEGRITY_FAILURE | post-copy validation | RAW_REMOVED"`n`n            $2',1)

# C03
$CalendarFunction = @'
function Test-ExpectedNoDataDate {
    param([Parameter(Mandatory = $true)][datetime]$Date)
    return $Date.DayOfWeek -eq [DayOfWeek]::Saturday -or $Date.DayOfWeek -eq [DayOfWeek]::Sunday
}

'@
if (-not $Text.Contains('function Process-Day {')) { throw 'Process-Day function not found' }
if (-not $Text.Contains('function Test-ExpectedNoDataDate')) { $Text = $Text.Replace('function Process-Day {',$CalendarFunction + 'function Process-Day {') }
$EmptyPattern = '(?ms)        if \(\$CsvFiles\.Count -eq 0\)\s*\{.*?return "NO_DATA"\s*\n        \}'
$EmptyReplacement = @'
        if ($CsvFiles.Count -eq 0) {
            if (Test-ExpectedNoDataDate -Date $Date) {
                Write-Log "$DateString | NO_DATA | aucun CSV | EXPECTED_CLOSED_MARKET_DAY"
                Add-ManifestRecord -Date $Date -Status "NO_DATA" -File "" -Validation "NO_CSV_OUTPUT_EXPECTED_CLOSED_MARKET_DAY"
                return "NO_DATA"
            }
            throw "EMPTY_DOWNLOAD: dukascopy-node returned exit 0 but produced no CSV on a non-expected closed-market day."
        }
'@
if (-not [regex]::IsMatch($Text,$EmptyPattern)) { throw 'C03 original empty-output block not found' }
$Text = [regex]::Replace($Text,$EmptyPattern,$EmptyReplacement,1)

# H03: use a direct source insertion anchored on the exact original line.
$OldNodeLine = '$NodeVersion = (& node --version).Trim()'
if (-not $Text.Contains($OldNodeLine)) { throw 'H03 original node line not found' }
$NodeBlock = @'
$NodeVersion = "UNKNOWN"
try {
    $NodeVersion = (& node --version 2>$null).Trim()
    if ([string]::IsNullOrWhiteSpace($NodeVersion)) { throw "node --version returned empty output" }
}
catch {
    Write-Error "NODE_RUNTIME_UNAVAILABLE: $($_.Exception.Message)"
    exit 1
}
'@
$Text = $Text.Replace($OldNodeLine,$NodeBlock.TrimEnd())

# M02
if ($Text -match 'Ã') {
    $Cp1252 = [Text.Encoding]::GetEncoding(1252)
    $Text = [Text.Encoding]::UTF8.GetString($Cp1252.GetBytes($Text))
}
if ($Text -match 'Ã.') { throw 'M02_MOJIBAKE_REMAINS' }
[IO.File]::WriteAllText($Source,$Text,(New-Object Text.UTF8Encoding($false)))

$NewBlob = (git hash-object $Source).Trim()
if ($NewBlob -eq $ExpectedOldBlob) { throw 'Patch produced no source change.' }
$Checks = [ordered]@{
    C01 = $Text.Contains('if ($Timestamp -lt $PreviousTimestamp)') -and -not $Text.Contains('if ($Timestamp -le $PreviousTimestamp)')
    C02 = $Text.Contains('SKIP_RAW_HASH_MISMATCH') -and $Text.Contains('Get-FileHash -LiteralPath $RawPath -Algorithm SHA256')
    C03 = $Text.Contains('EMPTY_DOWNLOAD: dukascopy-node returned exit 0 but produced no CSV')
    C04 = $Text.Contains('RAW_REMOVED')
    H03 = $Text.Contains('NODE_RUNTIME_UNAVAILABLE') -and $Text.Contains('$NodeVersion = "UNKNOWN"')
    M01 = -not $Text.Contains('$Matches = @(')
    M03 = $Text.Contains('[IO.Path]::GetTempPath()')
    M02 = -not ($Text -match 'Ã.')
}
foreach ($k in $Checks.Keys) { if (-not $Checks[$k]) { throw "ASSERTION FAILED: $k" } }
$Errors = $null
[void][System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path $Source),[ref]$null,[ref]$Errors)
if ($null -ne $Errors -and $Errors.Count -gt 0) { throw "PowerShell parser errors: $($Errors.Count)" }
Write-Host 'V3.3 CORRECTION PATCH PREPARED'
Write-Host "SOURCE=$Source"
Write-Host "BACKUP=$Backup"
Write-Host "OLD_BLOB=$ExpectedOldBlob"
Write-Host "NEW_BLOB=$NewBlob"
Write-Host 'C01=C02=C03=C04=H03=M01=M02=M03=PASS'
Write-Host 'RUNTIME QUALIFICATION REMAINS BLOCKED UNTIL AUTONOMOUS HARNESS EXECUTION.'