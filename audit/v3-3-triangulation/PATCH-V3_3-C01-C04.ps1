Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Repo = (Get-Location).Path
$Source = Join-Path $Repo 'audit\v3-3-triangulation\source\download_ticks_v3_3.ps1'
$ExpectedOldBlob = '3dc826146c527d7e2d1d51c4879b2b61c1c01dd7'

if (-not (Test-Path -LiteralPath $Source)) { throw "Source absent: $Source" }

$Bytes = [IO.File]::ReadAllBytes($Source)
$Text = [Text.Encoding]::UTF8.GetString($Bytes)
$ActualBlob = (git hash-object $Source).Trim()
if ($ActualBlob -ne $ExpectedOldBlob) { throw "Refus de patch: blob inattendu. Attendu=$ExpectedOldBlob Actuel=$ActualBlob" }

$Backup = "$Source.bak_before_C01_C04_$(Get-Date -Format yyyyMMdd_HHmmss)"
Copy-Item -LiteralPath $Source -Destination $Backup -Force

function Replace-Once([string]$Old,[string]$New,[string]$Id) {
    $script:Text = $script:Text.Replace($Old,$New)
    if (-not $script:Text.Contains($New)) { throw "Replacement failed: $Id" }
}

# C-01: equal millisecond timestamps are valid; only backward time is invalid.
Replace-Once 'if ($Timestamp -le $PreviousTimestamp) {' 'if ($Timestamp -lt $PreviousTimestamp) {' 'C01_MONOTONICITY'
Replace-Once '"Chronologie non strictement croissante : "' '"Chronologie décroissante : "' 'C01_MESSAGE'

# M-01: do not shadow PowerShell automatic variable $Matches.
Replace-Once '$Matches = @(' '$MatchingRecords = @(' 'M01_ASSIGN'
Replace-Once 'if ($Matches.Count -eq 0) {' 'if ($MatchingRecords.Count -eq 0) {' 'M01_EMPTY'
Replace-Once 'return $Matches[-1]' 'return $MatchingRecords[-1]' 'M01_RETURN'

# M-03: deterministic temp root on Windows and PowerShell Core.
Replace-Once '$TempRoot = Join-Path `n        $env:TEMP `n        ("dukascopy_v3_3_" + $RunId + "_" + $DateString)' '$TempBase = if ([string]::IsNullOrWhiteSpace($env:TEMP)) { [IO.Path]::GetTempPath() } else { $env:TEMP }`n    $TempRoot = Join-Path `n        $TempBase `n        ("dukascopy_v3_3_" + $RunId + "_" + $DateString)' 'M03_TEMP'

# C-02: SKIP is allowed only when the RAW matches the persistent VALID proof.
$OldSkip = @'
        Write-Log "$DateString | SKIP | déjà VALID"

        Add-ManifestRecord `
            -Date $Date `
            -Status "SKIP" `
            -File $RawPath `
            -Validation "ALREADY_VALID"

        return "SKIP"
'@
$NewSkip = @'
        if ([string]::IsNullOrWhiteSpace([string]$LatestValid.sha256) -or
            [string]::IsNullOrWhiteSpace([string]$LatestValid.file_size_bytes)) {
            Add-ManifestRecord `
                -Date $Date `
                -Status "BLOCKED" `
                -File $RawPath `
                -Validation "VALID_PROOF_INCOMPLETE" `
                -ErrorMessage "Le record VALID ne contient pas une preuve SHA-256/taille exploitable."
            return "BLOCKED"
        }

        $CurrentRawInfo = Get-Item -LiteralPath $RawPath
        $CurrentRawHash = (Get-FileHash -LiteralPath $RawPath -Algorithm SHA256).Hash
        if ([int64]$CurrentRawInfo.Length -ne [int64]$LatestValid.file_size_bytes -or
            $CurrentRawHash -ne [string]$LatestValid.sha256) {
            Add-ManifestRecord `
                -Date $Date `
                -Status "INTEGRITY_FAILURE" `
                -File $RawPath `
                -FileSizeBytes $CurrentRawInfo.Length `
                -Sha256 $CurrentRawHash `
                -Validation "SKIP_RAW_HASH_MISMATCH" `
                -ErrorMessage "RAW présent mais différent de la preuve VALID persistée."
            Write-Log "$DateString | INTEGRITY_FAILURE | SKIP_RAW_HASH_MISMATCH"
            return "INTEGRITY_FAILURE"
        }

        Write-Log "$DateString | SKIP | déjà VALID et hash vérifié"

        Add-ManifestRecord `
            -Date $Date `
            -Status "SKIP" `
            -File $RawPath `
            -FileSizeBytes $CurrentRawInfo.Length `
            -TickCount $LatestValid.tick_count `
            -Sha256 $CurrentRawHash `
            -FirstTimestamp $LatestValid.first_timestamp `
            -LastTimestamp $LatestValid.last_timestamp `
            -Validation "ALREADY_VALID_HASH_VERIFIED"

        return "SKIP"
'@
Replace-Once $OldSkip $NewSkip 'C02_SKIP_INTEGRITY'

# C-04: every post-copy integrity failure removes the untrusted RAW before returning.
$OldPost = @'
            Write-Log (
                "$DateString | INTEGRITY_FAILURE | " +
                "post-copy validation"
            )

            return "INTEGRITY_FAILURE"
'@
$NewPost = @'
            Remove-Item -LiteralPath $RawPath -Force -ErrorAction Stop
            Write-Log (
                "$DateString | INTEGRITY_FAILURE | post-copy validation | RAW_REMOVED"
            )

            return "INTEGRITY_FAILURE"
'@
Replace-Once $OldPost $NewPost 'C04_POST_VALIDATION'

$OldSize = @'
            Write-Log (
                "$DateString | INTEGRITY_FAILURE | SIZE_MISMATCH"
            )

            return "INTEGRITY_FAILURE"
'@
$NewSize = @'
            Remove-Item -LiteralPath $RawPath -Force -ErrorAction Stop
            Write-Log (
                "$DateString | INTEGRITY_FAILURE | SIZE_MISMATCH | RAW_REMOVED"
            )

            return "INTEGRITY_FAILURE"
'@
Replace-Once $OldSize $NewSize 'C04_SIZE'

$OldHash = @'
            Write-Log (
                "$DateString | INTEGRITY_FAILURE | SHA256_MISMATCH"
            )

            return "INTEGRITY_FAILURE"
'@
$NewHash = @'
            Remove-Item -LiteralPath $RawPath -Force -ErrorAction Stop
            Write-Log (
                "$DateString | INTEGRITY_FAILURE | SHA256_MISMATCH | RAW_REMOVED"
            )

            return "INTEGRITY_FAILURE"
'@
Replace-Once $OldHash $NewHash 'C04_HASH'

# C-03: an empty successful downloader result is not silently classified as NO_DATA.
# NO_DATA remains reserved for an explicitly expected closed-market day; an empty result
# on a potentially active day is a hard failure requiring investigation.
$Marker = 'function Process-Day {'
$CalendarFunction = @'
function Test-ExpectedNoDataDate {
    param([Parameter(Mandatory = $true)][datetime]$Date)
    return $Date.DayOfWeek -eq [DayOfWeek]::Saturday -or
           $Date.DayOfWeek -eq [DayOfWeek]::Sunday
}

'@
if (-not $Text.Contains('function Test-ExpectedNoDataDate')) {
    $Text = $Text.Replace($Marker,$CalendarFunction + $Marker)
}
$OldEmpty = @'
        if ($CsvFiles.Count -eq 0) {

            Write-Log (
                "$DateString | NO_DATA | aucun CSV"
            )

            Add-ManifestRecord `
                -Date $Date `
                -Status "NO_DATA" `
                -File "" `
                -Validation "NO_CSV_OUTPUT"

            return "NO_DATA"
        }
'@
$NewEmpty = @'
        if ($CsvFiles.Count -eq 0) {

            if (Test-ExpectedNoDataDate -Date $Date) {
                Write-Log "$DateString | NO_DATA | aucun CSV | EXPECTED_CLOSED_MARKET_DAY"
                Add-ManifestRecord `
                    -Date $Date `
                    -Status "NO_DATA" `
                    -File "" `
                    -Validation "NO_CSV_OUTPUT_EXPECTED_CLOSED_MARKET_DAY"
                return "NO_DATA"
            }

            throw "EMPTY_DOWNLOAD: dukascopy-node returned exit 0 but produced no CSV on a non-expected closed-market day."
        }
'@
Replace-Once $OldEmpty $NewEmpty 'C03_EMPTY_DOWNLOAD'

# H-03: node version check must be explicit and must not die outside the per-day try/catch.
$OldNode = '$NodeVersion = (& node --version).Trim()'
$NewNode = @'
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
Replace-Once $OldNode $NewNode 'H03_NODE_CHECK'

# M-02: write UTF-8 consistently; source is normalized as UTF-8 without a BOM.
$Text = $Text.Replace('SchÃ©ma','Schéma').Replace('Ã ','à').Replace('gÃ©nÃ©rique','générique').Replace('dÃ©terminer','déterminer').Replace('dÃ©but','début').Replace('numÃ©rique','numérique').Replace('violÃ©','violé').Replace('nÃ©gatif','négatif').Replace('Ã©crasement','écrasement')

[IO.File]::WriteAllText($Source,$Text,(New-Object Text.UTF8Encoding($false)))

$NewBlob = (git hash-object $Source).Trim()
if ($NewBlob -eq $ExpectedOldBlob) { throw 'Patch produced no blob change.' }

# Structural assertions required before commit.
$Checks = @{
  C01 = $Text.Contains('if ($Timestamp -lt $PreviousTimestamp)') -and -not $Text.Contains('if ($Timestamp -le $PreviousTimestamp)')
  C02 = $Text.Contains('SKIP_RAW_HASH_MISMATCH') -and $Text.Contains('Get-FileHash -LiteralPath $RawPath -Algorithm SHA256')
  C03 = $Text.Contains('EMPTY_DOWNLOAD: dukascopy-node returned exit 0 but produced no CSV')
  C04 = $Text.Contains('RAW_REMOVED')
  H03 = $Text.Contains('NODE_RUNTIME_UNAVAILABLE')
  M01 = -not $Text.Contains('$Matches = @(')
  M03 = $Text.Contains('[IO.Path]::GetTempPath()')
}
foreach ($k in $Checks.Keys) { if (-not $Checks[$k]) { throw "ASSERTION FAILED: $k" } }

$Syntax = $null
if (Get-Command pwsh -ErrorAction SilentlyContinue) {
  $Errors = $null
  [void][System.Management.Automation.Language.Parser]::ParseFile($Source,[ref]$null,[ref]$Errors)
  if ($null -ne $Errors -and $Errors.Count -gt 0) { throw "PowerShell parser errors: $($Errors.Count)" }
  $Syntax = 'PASS'
} else {
  $Syntax = 'BLOCKED_NO_PWSH'
}

Write-Host 'V3.3 CORRECTION PATCH PREPARED'
Write-Host "SOURCE=$Source"
Write-Host "BACKUP=$Backup"
Write-Host "OLD_BLOB=$ExpectedOldBlob"
Write-Host "NEW_BLOB=$NewBlob"
Write-Host "SYNTAX=$Syntax"
$Checks.GetEnumerator() | Sort-Object Name | ForEach-Object { Write-Host "$($_.Key)=$($_.Value)" }
Write-Host 'IMPORTANT: this script modifies only the audit-branch source. Runtime qualification remains BLOCKED until the autonomous harness executes.'
