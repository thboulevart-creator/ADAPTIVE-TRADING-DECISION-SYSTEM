Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Repo = (Get-Location).Path
$Source = Join-Path $Repo 'audit\v3-3-triangulation\source\download_ticks_v3_3.ps1'
$ExpectedOldBlob = '3dc826146c527d7e2d1d51c4879b2b61c1c01dd7'
if (-not (Test-Path -LiteralPath $Source)) { throw "Source absent: $Source" }
$Text = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($Source))
$ActualBlob = (git hash-object $Source).Trim()
if ($ActualBlob -ne $ExpectedOldBlob) { throw "Refus de patch: blob inattendu. Attendu=$ExpectedOldBlob Actuel=$ActualBlob" }

$Backup = "$Source.bak_before_C01_C04_$(Get-Date -Format yyyyMMdd_HHmmss)"
Copy-Item -LiteralPath $Source -Destination $Backup -Force

function Replace-RegexOnce([string]$Pattern,[string]$Replacement,[string]$Id) {
    $m = [regex]::Matches($script:Text,$Pattern)
    if ($m.Count -ne 1) { throw "Expected exactly one match for $Id, got $($m.Count)" }
    $script:Text = [regex]::Replace($script:Text,$Pattern,$Replacement,1)
}

Replace-RegexOnce '\$Timestamp\s+-le\s+\$PreviousTimestamp' '$Timestamp -lt $PreviousTimestamp' 'C01_MONOTONICITY'
$Text = $Text.Replace('Chronologie non strictement croissante :','Chronologie décroissante :')

$Text = $Text.Replace('$Matches = @(', '$MatchingRecords = @(')
$Text = $Text.Replace('$Matches.Count', '$MatchingRecords.Count')
$Text = $Text.Replace('$Matches[-1]', '$MatchingRecords[-1]')
if ($Text.Contains('$Matches = @(')) { throw 'M01 replacement incomplete' }

$TempPattern = '(?ms)\$TempRoot\s*=\s*Join-Path\s+`\s*\$env:TEMP\s+`\s*\(\"dukascopy_v3_3_\"\s*\+\s*\$RunId\s*\+\s*\"_\"\s*\+\s*\$DateString\)'
$TempReplacement = '$TempBase = if ([string]::IsNullOrWhiteSpace($env:TEMP)) { [IO.Path]::GetTempPath() } else { $env:TEMP }`n    $TempRoot = Join-Path $TempBase ("dukascopy_v3_3_" + $RunId + "_" + $DateString)'
Replace-RegexOnce $TempPattern $TempReplacement 'M03_TEMP'

$SkipPattern = '(?ms)        Write-Log "\$DateString \| SKIP \| déjà VALID".*?        return "SKIP"'
$SkipReplacement = @'
        if ([string]::IsNullOrWhiteSpace([string]$LatestValid.sha256) -or
            [string]::IsNullOrWhiteSpace([string]$LatestValid.file_size_bytes)) {
            Add-ManifestRecord -Date $Date -Status "BLOCKED" -File $RawPath -Validation "VALID_PROOF_INCOMPLETE" -ErrorMessage "Preuve VALID SHA-256/taille absente ou inexploitable."
            return "BLOCKED"
        }

        $CurrentRawInfo = Get-Item -LiteralPath $RawPath
        $CurrentRawHash = (Get-FileHash -LiteralPath $RawPath -Algorithm SHA256).Hash
        if ([int64]$CurrentRawInfo.Length -ne [int64]$LatestValid.file_size_bytes -or
            $CurrentRawHash -ne [string]$LatestValid.sha256) {
            Add-ManifestRecord -Date $Date -Status "INTEGRITY_FAILURE" -File $RawPath -FileSizeBytes $CurrentRawInfo.Length -Sha256 $CurrentRawHash -Validation "SKIP_RAW_HASH_MISMATCH" -ErrorMessage "RAW différent de la preuve VALID persistée."
            Write-Log "$DateString | INTEGRITY_FAILURE | SKIP_RAW_HASH_MISMATCH"
            return "INTEGRITY_FAILURE"
        }

        Write-Log "$DateString | SKIP | déjà VALID et hash vérifié"
        Add-ManifestRecord -Date $Date -Status "SKIP" -File $RawPath -FileSizeBytes $CurrentRawInfo.Length -TickCount $LatestValid.tick_count -Sha256 $CurrentRawHash -FirstTimestamp $LatestValid.first_timestamp -LastTimestamp $LatestValid.last_timestamp -Validation "ALREADY_VALID_HASH_VERIFIED"
        return "SKIP"'@
Replace-RegexOnce $SkipPattern $SkipReplacement 'C02_SKIP_INTEGRITY'

$PostPattern = '(?ms)(\$PostValidation\.Status -ne "VALID"\)\s*\{.*?Write-Log \(\s*"\$DateString \| INTEGRITY_FAILURE \| " \+\s*"post-copy validation"\s*\)\s*)(return "INTEGRITY_FAILURE")'
if (-not [regex]::IsMatch($Text,$PostPattern)) { throw 'C04 post-copy block not found' }
$Text = [regex]::Replace($Text,$PostPattern,'$1Remove-Item -LiteralPath $RawPath -Force -ErrorAction Stop`n`n            Write-Log "$DateString | INTEGRITY_FAILURE | post-copy validation | RAW_REMOVED"`n`n            $2',1)

$SizePattern = '(?ms)(\$PreValidation\.FileSizeBytes -ne\s*\$PostValidation\.FileSizeBytes\)\s*\{.*?Write-Log \(\s*"\$DateString \| INTEGRITY_FAILURE \| SIZE_MISMATCH"\s*\)\s*)(return "INTEGRITY_FAILURE")'
if ([regex]::IsMatch($Text,$SizePattern)) { $Text = [regex]::Replace($Text,$SizePattern,'$1Remove-Item -LiteralPath $RawPath -Force -ErrorAction Stop`n`n            Write-Log "$DateString | INTEGRITY_FAILURE | SIZE_MISMATCH | RAW_REMOVED"`n`n            $2',1) }
$HashPattern = '(?ms)(\$PreValidation\.Sha256 -ne\s*\$PostValidation\.Sha256\)\s*\{.*?Write-Log \(\s*"\$DateString \| INTEGRITY_FAILURE \| SHA256_MISMATCH"\s*\)\s*)(return "INTEGRITY_FAILURE")'
if ([regex]::IsMatch($Text,$HashPattern)) { $Text = [regex]::Replace($Text,$HashPattern,'$1Remove-Item -LiteralPath $RawPath -Force -ErrorAction Stop`n`n            Write-Log "$DateString | INTEGRITY_FAILURE | SHA256_MISMATCH | RAW_REMOVED"`n`n            $2',1) }

if (-not $Text.Contains('function Test-ExpectedNoDataDate')) {
    $Text = $Text.Replace('function Process-Day {', @'
function Test-ExpectedNoDataDate {
    param([Parameter(Mandatory = $true)][datetime]$Date)
    return $Date.DayOfWeek -eq [DayOfWeek]::Saturday -or $Date.DayOfWeek -eq [DayOfWeek]::Sunday
}

function Process-Day {'@)
}
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
Replace-RegexOnce $EmptyPattern $EmptyReplacement 'C03_EMPTY_DOWNLOAD'

Replace-RegexOnce '^\$NodeVersion\s*=\s*\(& node --version\)\.Trim\(\)\s*$' @'
$NodeVersion = "UNKNOWN"
try {
    $NodeVersion = (& node --version 2>$null).Trim()
    if ([string]::IsNullOrWhiteSpace($NodeVersion)) { throw "node --version returned empty output" }
}
catch {
    Write-Error "NODE_RUNTIME_UNAVAILABLE: $($_.Exception.Message)"
    exit 1
}
'@ 'H03_NODE_CHECK'

$Fixes = @{
 'journÃ©e'='journée'; 'numÃ©rique'='numérique'; 'violÃ©'='violé'; 'nÃ©gatif'='négatif'; 'Ã©crasement'='écrasement'; 'Aucun Ã©crasement'='Aucun écrasement'; 'dÃ©but'='début'; 'gÃ©nÃ©rique'='générique'; 'SchÃ©ma'='Schéma'
}
foreach ($kv in $Fixes.GetEnumerator()) { $Text = $Text.Replace($kv.Key,$kv.Value) }
if ($Text -match 'Ã.') { throw 'M02_MOJIBAKE_REMAINS' }
[IO.File]::WriteAllText($Source,$Text,(New-Object Text.UTF8Encoding($false)))

$NewBlob = (git hash-object $Source).Trim()
if ($NewBlob -eq $ExpectedOldBlob) { throw 'Patch produced no blob change.' }

$Checks = [ordered]@{
 C01 = $Text.Contains('$Timestamp -lt $PreviousTimestamp') -and -not $Text.Contains('$Timestamp -le $PreviousTimestamp')
 C02 = $Text.Contains('SKIP_RAW_HASH_MISMATCH') -and $Text.Contains('Get-FileHash -LiteralPath $RawPath -Algorithm SHA256')
 C03 = $Text.Contains('EMPTY_DOWNLOAD: dukascopy-node returned exit 0 but produced no CSV') -and $Text.Contains('EXPECTED_CLOSED_MARKET_DAY')
 C04 = $Text.Contains('RAW_REMOVED')
 H03 = $Text.Contains('NODE_RUNTIME_UNAVAILABLE')
 M01 = -not $Text.Contains('$Matches = @(')
 M03 = $Text.Contains('[IO.Path]::GetTempPath()')
 M02 = -not ($Text -match 'Ã.')
}
foreach ($k in $Checks.Keys) { if (-not $Checks[$k]) { throw "ASSERTION FAILED: $k" } }
$Errors = $null
[void][System.Management.Automation.Language.Parser]::ParseFile($Source,[ref]$null,[ref]$Errors)
if ($null -ne $Errors -and $Errors.Count -gt 0) { throw "PowerShell parser errors: $($Errors.Count)" }

Write-Host 'V3.3 CORRECTION PATCH PREPARED'
Write-Host "SOURCE=$Source"
Write-Host "BACKUP=$Backup"
Write-Host "OLD_BLOB=$ExpectedOldBlob"
Write-Host "NEW_BLOB=$NewBlob"
$Checks.GetEnumerator() | ForEach-Object { Write-Host "$($_.Key)=$($_.Value)" }
Write-Host 'Runtime qualification remains separate and must be evidenced by the autonomous harness.'
