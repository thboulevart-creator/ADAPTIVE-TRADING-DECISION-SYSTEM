?Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ============================================================
# DOWNLOAD TICKS V3.3
# ============================================================
# Purpose:
#   Controlled acquisition of Dukascopy raw ticks.
#
# IMPORTANT:
#   This version is a TEST / VALIDATION runner.
#   DO NOT launch the 10-year acquisition before all gates pass.
#
# Design principles:
#   - RAW is immutable once a VALID dataset exists.
#   - Every day has one terminal status.
#   - No control-flow instruction may bypass date advancement.
#   - Data is validated before and after RAW copy.
#   - Provenance and SHA-256 are recorded.
# ============================================================


# ============================================================
# 1. CONFIGURATION
# ============================================================

$Instrument = "usatechidxusd"
$Timeframe  = "tick"
$Volumes    = $true

# Controlled test window ONLY.
$StartDate = [datetime]::ParseExact(
    "2026-01-02",
    "yyyy-MM-dd",
    [Globalization.CultureInfo]::InvariantCulture
)

$EndDate = [datetime]::ParseExact(
    "2026-01-07",
    "yyyy-MM-dd",
    [Globalization.CultureInfo]::InvariantCulture
)

$DukascopyNodeVersion = "1.50.0"

$RawRoot        = Join-Path (Get-Location) "RAW\USATECH.IDX-USD\TICK"
$ManifestRoot   = Join-Path (Get-Location) "MANIFEST"
$LogRoot        = Join-Path (Get-Location) "LOGS"
$ValidationRoot = Join-Path (Get-Location) "VALIDATION"

$ManifestPath = Join-Path $ManifestRoot "manifest_v3_3.csv"

$RunnerPath = $MyInvocation.MyCommand.Path

if ([string]::IsNullOrWhiteSpace($RunnerPath)) {
    throw "Impossible de déterminer le chemin du runner."
}

$RunnerResolved = (Resolve-Path $RunnerPath).Path
$RunnerHash = (Get-FileHash $RunnerResolved -Algorithm SHA256).Hash

$RunId = [guid]::NewGuid().ToString()

$RunStartUtc = [datetime]::UtcNow.ToString(
    "yyyy-MM-ddTHH:mm:ss.fffZ"
)

$LogPath = Join-Path `
    $LogRoot `
    ("download_ticks_v3_3_" + $RunId + ".log")

$MetadataPath = Join-Path `
    $ValidationRoot `
    ("run_" + $RunId + "_metadata.json")


# ============================================================
# 2. EXPECTED RAW SCHEMA
# ============================================================

$ExpectedColumns = @(
    "timestamp",
    "askPrice",
    "bidPrice",
    "askVolume",
    "bidVolume"
)


# ============================================================
# 3. DIRECTORY INITIALIZATION
# ============================================================

New-Item -ItemType Directory -Force $RawRoot        | Out-Null
New-Item -ItemType Directory -Force $ManifestRoot   | Out-Null
New-Item -ItemType Directory -Force $LogRoot        | Out-Null
New-Item -ItemType Directory -Force $ValidationRoot | Out-Null


# ============================================================
# 4. LOGGING
# ============================================================

function Write-Log {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message
    )

    $Utc = [datetime]::UtcNow.ToString(
        "yyyy-MM-dd HH:mm:ss.fff"
    )

    $Line = "$Utc | $Message"

    Add-Content `
        -LiteralPath $LogPath `
        -Value $Line `
        -Encoding UTF8

    Write-Host $Line
}


# ============================================================
# 5. MANIFEST
# ============================================================

$ManifestColumns = @(
    "event_utc",
    "run_id",
    "date",
    "status",
    "instrument",
    "timeframe",
    "file",
    "file_size_bytes",
    "tick_count",
    "sha256",
    "first_timestamp",
    "last_timestamp",
    "validation",
    "error"
)

if (-not (Test-Path -LiteralPath $ManifestPath)) {

    ($ManifestColumns -join ",") |
        Set-Content `
            -LiteralPath $ManifestPath `
            -Encoding UTF8
}


function Get-LatestManifestRecord {

    param(
        [Parameter(Mandatory = $true)]
        [datetime]$Date
    )

    if (-not (Test-Path -LiteralPath $ManifestPath)) {
        return $null
    }

    $Records = Import-Csv `
        -LiteralPath $ManifestPath

    $DateString = $Date.ToString("yyyy-MM-dd")

    $MatchingRecords = @(
        $Records |
        Where-Object {
            $_.date -eq $DateString
        }
    )

    if ($MatchingRecords.Count -eq 0) {
        return $null
    }

    return $MatchingRecords[-1]
}


function Get-LatestValidManifestRecord {

    param(
        [Parameter(Mandatory = $true)]
        [datetime]$Date
    )

    if (-not (Test-Path -LiteralPath $ManifestPath)) {
        return $null
    }

    $DateString = $Date.ToString("yyyy-MM-dd")

    $Records = @(
        Import-Csv -LiteralPath $ManifestPath |
        Where-Object {
            $_.date -eq $DateString -and
            $_.status -eq "VALID"
        }
    )

    if ($Records.Count -eq 0) {
        return $null
    }

    return $Records[-1]
}
function Add-ManifestRecord {

    param(
        [Parameter(Mandatory = $true)]
        [datetime]$Date,

        [Parameter(Mandatory = $true)]
        [string]$Status,

        [string]$File = "",

        [string]$FileSizeBytes = "",

        [string]$TickCount = "",

        [string]$Sha256 = "",

        [string]$FirstTimestamp = "",

        [string]$LastTimestamp = "",

        [string]$Validation = "",

        [string]$ErrorMessage = ""
    )

    $Record = [pscustomobject]@{
        event_utc       = [datetime]::UtcNow.ToString(
                              "yyyy-MM-ddTHH:mm:ss.fffZ"
                          )
        run_id          = $RunId
        date            = $Date.ToString("yyyy-MM-dd")
        status          = $Status
        instrument      = $Instrument
        timeframe       = $Timeframe
        file            = $File
        file_size_bytes = $FileSizeBytes
        tick_count      = $TickCount
        sha256          = $Sha256
        first_timestamp = $FirstTimestamp
        last_timestamp  = $LastTimestamp
        validation      = $Validation
        error           = $ErrorMessage
    }

    $Record |
        ConvertTo-Csv -NoTypeInformation |
        Select-Object -Skip 1 |
        Add-Content `
            -LiteralPath $ManifestPath `
            -Encoding UTF8
}


# ============================================================
# 6. RAW PATH
# ============================================================

function Get-RawPath {

    param(
        [Parameter(Mandatory = $true)]
        [datetime]$Date
    )

    $Year  = $Date.ToString("yyyy")
    $Month = $Date.ToString("MM")
    $Day   = $Date.ToString("yyyy-MM-dd")

    $Directory = Join-Path `
        $RawRoot `
        "$Year\$Month"

    New-Item `
        -ItemType Directory `
        -Force `
        -Path $Directory |
        Out-Null

    return Join-Path `
        $Directory `
        "$Day.csv"
}


# ============================================================
# 7. DAY BOUNDARIES
# ============================================================

function Get-DayBounds {

    param(
        [Parameter(Mandatory = $true)]
        [datetime]$Date
    )

    $DayStartUtc = [datetime]::SpecifyKind(
        $Date.Date,
        [DateTimeKind]::Utc
    )

    $DayEndUtc = $DayStartUtc.AddDays(1)

    $UnixEpoch = [datetime]::SpecifyKind(
        [datetime]::Parse(
            "1970-01-01",
            [Globalization.CultureInfo]::InvariantCulture
        ),
        [DateTimeKind]::Utc
    )

    $StartMs = [int64](
        ($DayStartUtc - $UnixEpoch).TotalMilliseconds
    )

    $EndMs = [int64](
        ($DayEndUtc - $UnixEpoch).TotalMilliseconds
    )

    return [pscustomobject]@{
        StartUtc = $DayStartUtc
        EndUtc   = $DayEndUtc
        StartMs  = $StartMs
        EndMs    = $EndMs
    }
}


# ============================================================
# 8. TICK FILE VALIDATOR
# ============================================================

function Test-TickFile {

    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [datetime]$Date
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Fichier absent : $Path"
    }

    $FileInfo = Get-Item -LiteralPath $Path

    if ($FileInfo.Length -le 0) {
        return [pscustomobject]@{
            Status          = "NO_DATA"
            FileSizeBytes   = 0
            TickCount       = 0
            Sha256          = ""
            FirstTimestamp  = ""
            LastTimestamp   = ""
            Validation      = "EMPTY_FILE"
        }
    }

    $Rows = @(Import-Csv -LiteralPath $Path)

    if ($Rows.Count -eq 0) {
        return [pscustomobject]@{
            Status          = "NO_DATA"
            FileSizeBytes   = $FileInfo.Length
            TickCount       = 0
            Sha256          = ""
            FirstTimestamp  = ""
            LastTimestamp   = ""
            Validation      = "EMPTY_CSV"
        }
    }

    # --------------------------------------------------------
    # Exact schema: same number + same order + same names.
    # --------------------------------------------------------

    $ActualColumns = @(
        $Rows[0].PSObject.Properties.Name
    )

    if ($ActualColumns.Count -ne $ExpectedColumns.Count) {
        throw (
            "Schéma invalide : nombre de colonnes attendu=" +
            $ExpectedColumns.Count +
            ", obtenu=" +
            $ActualColumns.Count
        )
    }

    for ($ColumnIndex = 0;
         $ColumnIndex -lt $ExpectedColumns.Count;
         $ColumnIndex++) {

        if ($ActualColumns[$ColumnIndex] -ne
            $ExpectedColumns[$ColumnIndex]) {

            throw (
                "Schéma invalide à la colonne " +
                $ColumnIndex +
                " : attendu='" +
                $ExpectedColumns[$ColumnIndex] +
                "', obtenu='" +
                $ActualColumns[$ColumnIndex] +
                "'"
            )
        }
    }


    # --------------------------------------------------------
    # Explicit OHLC contamination check.
    # --------------------------------------------------------

    $ForbiddenColumns = @(
        "open",
        "high",
        "low",
        "close",
        "volume"
    )

    foreach ($Forbidden in $ForbiddenColumns) {

        if ($ActualColumns -contains $Forbidden) {
            throw (
                "Colonne OHLC/volume générique interdite détectée : " +
                $Forbidden
            )
        }
    }


    # --------------------------------------------------------
    # Date bounds.
    # --------------------------------------------------------

    $Bounds = Get-DayBounds -Date $Date

    $PreviousTimestamp = $null
    $FirstTimestamp = $null
    $LastTimestamp = $null


    # --------------------------------------------------------
    # Row validation.
    # --------------------------------------------------------

    foreach ($Row in $Rows) {

        $TimestampRaw = [string]$Row.timestamp

        if ([string]::IsNullOrWhiteSpace($TimestampRaw)) {
            throw "Timestamp vide."
        }

        $Timestamp = 0L

        if (-not [int64]::TryParse(
            $TimestampRaw,
            [Globalization.NumberStyles]::Integer,
            [Globalization.CultureInfo]::InvariantCulture,
            [ref]$Timestamp
        )) {
            throw "Timestamp non entier : $TimestampRaw"
        }

        # Unix milliseconds sanity check.
        if ($Timestamp -lt 1000000000000) {
            throw "Timestamp trop petit pour des millisecondes Unix : $Timestamp"
        }

        # Inclusive start, exclusive end.
        if ($Timestamp -lt $Bounds.StartMs) {
            throw (
                "Timestamp avant le début de la journée : " +
                $Timestamp
            )
        }

        if ($Timestamp -ge $Bounds.EndMs) {
            throw (
                "Timestamp hors limite de la journée : " +
                $Timestamp
            )
        }

        if ($null -eq $PreviousTimestamp) {
            $FirstTimestamp = $Timestamp
        }
        else {

            if ($Timestamp -lt $PreviousTimestamp) {
                throw (
                    "Chronologie d�croissante : " +
                    $PreviousTimestamp +
                    " -> " +
                    $Timestamp
                )
            }
        }

        $PreviousTimestamp = $Timestamp
        $LastTimestamp = $Timestamp


        # ----------------------------------------------------
        # Price validation.
        # ----------------------------------------------------

        $Ask = 0.0
        $Bid = 0.0

        if (-not [double]::TryParse(
            [string]$Row.askPrice,
            [Globalization.NumberStyles]::Float,
            [Globalization.CultureInfo]::InvariantCulture,
            [ref]$Ask
        )) {
            throw "askPrice non numérique : $($Row.askPrice)"
        }

        if (-not [double]::TryParse(
            [string]$Row.bidPrice,
            [Globalization.NumberStyles]::Float,
            [Globalization.CultureInfo]::InvariantCulture,
            [ref]$Bid
        )) {
            throw "bidPrice non numérique : $($Row.bidPrice)"
        }

        if ([double]::IsNaN($Ask) -or
            [double]::IsInfinity($Ask)) {
            throw "askPrice non fini : $Ask"
        }

        if ([double]::IsNaN($Bid) -or
            [double]::IsInfinity($Bid)) {
            throw "bidPrice non fini : $Bid"
        }

        if ($Ask -le 0 -or $Bid -le 0) {
            throw (
                "Prix non positifs : ask=$Ask bid=$Bid"
            )
        }

        if ($Ask -lt $Bid) {
            throw (
                "Invariant ask >= bid violé : ask=$Ask bid=$Bid"
            )
        }


        # ----------------------------------------------------
        # Volume validation.
        #
        # IMPORTANT:
        # These are preserved as source-provided Dukascopy
        # fields. They are NOT interpreted here as centralized
        # Nasdaq executed volume.
        # ----------------------------------------------------

        $AskVolume = 0.0
        $BidVolume = 0.0

        if (-not [double]::TryParse(
            [string]$Row.askVolume,
            [Globalization.NumberStyles]::Float,
            [Globalization.CultureInfo]::InvariantCulture,
            [ref]$AskVolume
        )) {
            throw "askVolume non numérique : $($Row.askVolume)"
        }

        if (-not [double]::TryParse(
            [string]$Row.bidVolume,
            [Globalization.NumberStyles]::Float,
            [Globalization.CultureInfo]::InvariantCulture,
            [ref]$BidVolume
        )) {
            throw "bidVolume non numérique : $($Row.bidVolume)"
        }

        if ([double]::IsNaN($AskVolume) -or
            [double]::IsInfinity($AskVolume)) {
            throw "askVolume non fini : $AskVolume"
        }

        if ([double]::IsNaN($BidVolume) -or
            [double]::IsInfinity($BidVolume)) {
            throw "bidVolume non fini : $BidVolume"
        }

        if ($AskVolume -lt 0 -or $BidVolume -lt 0) {
            throw (
                "Volume négatif : askVolume=$AskVolume " +
                "bidVolume=$BidVolume"
            )
        }
    }


    # --------------------------------------------------------
    # Hash calculated only after successful validation.
    # --------------------------------------------------------

    $Hash = (
        Get-FileHash `
            -LiteralPath $Path `
            -Algorithm SHA256
    ).Hash


    return [pscustomobject]@{
        Status          = "VALID"
        FileSizeBytes   = $FileInfo.Length
        TickCount       = $Rows.Count
        Sha256          = $Hash
        FirstTimestamp  = $FirstTimestamp
        LastTimestamp   = $LastTimestamp
        Validation      = "PASS"
    }
}


# ============================================================
# 9. SINGLE DAY PROCESSOR
# ============================================================

function Test-ExpectedNoDataDate {
    param([Parameter(Mandatory = $true)][datetime]$Date)
    return $Date.DayOfWeek -eq [DayOfWeek]::Saturday -or $Date.DayOfWeek -eq [DayOfWeek]::Sunday
}
function Process-Day {

    param(
        [Parameter(Mandatory = $true)]
        [datetime]$Date
    )

    $DateString = $Date.ToString("yyyy-MM-dd")
    $RawPath = Get-RawPath -Date $Date

    Write-Log "$DateString | PROCESS"

    # --------------------------------------------------------
    # Existing VALID record = immutable/idempotent skip.
    # --------------------------------------------------------
    # --------------------------------------------------------
    # Existing VALID proof = immutable/idempotent skip.
    #
    # IMPORTANT:
    # Search for a persistent VALID proof.
    # SKIP is only an execution event and must never hide VALID.
    # --------------------------------------------------------

    $LatestValid = Get-LatestValidManifestRecord -Date $Date

    if ($null -ne $LatestValid) {

        if (-not (Test-Path -LiteralPath $RawPath)) {

            Add-ManifestRecord `
                -Date $Date `
                -Status "BLOCKED" `
                -File $RawPath `
                -Validation "MISSING_RAW_FOR_VALID_MANIFEST" `
                -ErrorMessage "Manifest indique VALID mais RAW absent."

            Write-Log (
                "$DateString | BLOCKED | " +
                "VALID manifest mais RAW absent"
            )

            return "BLOCKED"
        }

        if ([string]::IsNullOrWhiteSpace([string]$LatestValid.sha256) -or [string]::IsNullOrWhiteSpace([string]$LatestValid.file_size_bytes)) {


            Add-ManifestRecord -Date $Date -Status "BLOCKED" -File $RawPath -Validation "VALID_PROOF_INCOMPLETE" -ErrorMessage "Le record VALID ne contient pas une preuve SHA-256/taille exploitable."


            return "BLOCKED"


        }


        $CurrentRawInfo = Get-Item -LiteralPath $RawPath


        $CurrentRawHash = (Get-FileHash -LiteralPath $RawPath -Algorithm SHA256).Hash


        if ([int64]$CurrentRawInfo.Length -ne [int64]$LatestValid.file_size_bytes -or $CurrentRawHash -ne [string]$LatestValid.sha256) {


            Add-ManifestRecord -Date $Date -Status "INTEGRITY_FAILURE" -File $RawPath -FileSizeBytes $CurrentRawInfo.Length -Sha256 $CurrentRawHash -Validation "SKIP_RAW_HASH_MISMATCH" -ErrorMessage "RAW pr�sent mais diff�rent de la preuve VALID persist�e."


            Write-Log "$DateString | INTEGRITY_FAILURE | SKIP_RAW_HASH_MISMATCH"


            return "INTEGRITY_FAILURE"


        }


        Write-Log "$DateString | SKIP | d�j� VALID et hash v�rifi�"


        Add-ManifestRecord -Date $Date -Status "SKIP" -File $RawPath -FileSizeBytes $CurrentRawInfo.Length -TickCount $LatestValid.tick_count -Sha256 $CurrentRawHash -FirstTimestamp $LatestValid.first_timestamp -LastTimestamp $LatestValid.last_timestamp -Validation "ALREADY_VALID_HASH_VERIFIED"


        return "SKIP"
    }



    # --------------------------------------------------------
    # Existing RAW without a VALID record:
    # NEVER overwrite automatically.
    # --------------------------------------------------------

    if (Test-Path -LiteralPath $RawPath) {

        Add-ManifestRecord `
            -Date $Date `
            -Status "BLOCKED" `
            -File $RawPath `
            -Validation "RAW_EXISTS_WITHOUT_VALID" `
            -ErrorMessage (
                "RAW existe sans preuve VALID correspondante. " +
                "Aucun écrasement automatique."
            )

        Write-Log (
            "$DateString | BLOCKED | RAW existe sans VALID"
        )

        return "BLOCKED"
    }


    # --------------------------------------------------------
    # Temporary download workspace.
    # --------------------------------------------------------

    $TempBase = if ([string]::IsNullOrWhiteSpace($env:TEMP)) { [IO.Path]::GetTempPath() } else { $env:TEMP }`n    $TempRoot = Join-Path `n        $TempBase `n        ("dukascopy_v3_3_" + $RunId + "_" + $DateString)

    if (Test-Path -LiteralPath $TempRoot) {
        Remove-Item `
            -LiteralPath $TempRoot `
            -Recurse `
            -Force
    }

    New-Item `
        -ItemType Directory `
        -Force `
        -LiteralPath $TempRoot |
        Out-Null


    try {

        # ----------------------------------------------------
        # Download.
        # ----------------------------------------------------

        Write-Log "$DateString | DOWNLOAD"

        $From = $Date.ToString("yyyy-MM-dd")
        $To   = $Date.AddDays(1).ToString("yyyy-MM-dd")

        & npx "dukascopy-node@$DukascopyNodeVersion" `
            -i $Instrument `
            -from $From `
            -to $To `
            -t tick `
            -f csv `
            -v `
            -dir $TempRoot

        $ExitCode = $LASTEXITCODE

        if ($ExitCode -ne 0) {

            throw (
                "dukascopy-node exit code = " +
                $ExitCode
            )
        }


        # ----------------------------------------------------
        # Discover output files.
        #
        # Exactly:
        #   0 files = NO_DATA
        #   1 file  = proceed
        #   >1      = FAILED/anomaly
        # ----------------------------------------------------

        $CsvFiles = @(
            Get-ChildItem `
                -LiteralPath $TempRoot `
                -Filter "*.csv" `
                -File
        )

        if ($CsvFiles.Count -eq 0) {
            if (Test-ExpectedNoDataDate -Date $Date) {
                Write-Log "$DateString | NO_DATA | aucun CSV | EXPECTED_CLOSED_MARKET_DAY"
                Add-ManifestRecord -Date $Date -Status "NO_DATA" -File "" -Validation "NO_CSV_OUTPUT_EXPECTED_CLOSED_MARKET_DAY"
                return "NO_DATA"
            }
            throw "EMPTY_DOWNLOAD: dukascopy-node returned exit 0 but produced no CSV on a non-expected closed-market day."
        }

        if ($CsvFiles.Count -gt 1) {

            throw (
                "Nombre inattendu de CSV : " +
                $CsvFiles.Count
            )
        }

        $DownloadedFile = $CsvFiles[0].FullName


        # ----------------------------------------------------
        # Pre-RAW validation.
        # ----------------------------------------------------

        $PreValidation = Test-TickFile `
            -Path $DownloadedFile `
            -Date $Date

        if ($PreValidation.Status -eq "NO_DATA") {

            Write-Log (
                "$DateString | NO_DATA | fichier CSV vide"
            )

            Add-ManifestRecord `
                -Date $Date `
                -Status "NO_DATA" `
                -File "" `
                -FileSizeBytes $PreValidation.FileSizeBytes `
                -TickCount 0 `
                -Validation $PreValidation.Validation

            return "NO_DATA"
        }


        # ----------------------------------------------------
        # RAW copy.
        #
        # Copy only after successful validation.
        # Never overwrite.
        # ----------------------------------------------------

        if (Test-Path -LiteralPath $RawPath) {
            throw (
                "RAW apparu avant copie : " +
                $RawPath
            )
        }

        Copy-Item `
            -LiteralPath $DownloadedFile `
            -Destination $RawPath `
            -ErrorAction Stop


        # ----------------------------------------------------
        # Post-RAW validation.
        # ----------------------------------------------------

        Write-Log (
            "$DateString | POST-COPY VALIDATION"
        )

        $PostValidation = Test-TickFile `
            -Path $RawPath `
            -Date $Date

        if ($PostValidation.Status -ne "VALID") {

            Add-ManifestRecord `
                -Date $Date `
                -Status "INTEGRITY_FAILURE" `
                -File $RawPath `
                -FileSizeBytes $PostValidation.FileSizeBytes `
                -TickCount $PostValidation.TickCount `
                -Sha256 $PostValidation.Sha256 `
                -FirstTimestamp $PostValidation.FirstTimestamp `
                -LastTimestamp $PostValidation.LastTimestamp `
                -Validation "POST_COPY_NOT_VALID" `
                -ErrorMessage (
                    "La validation post-copie n'est pas VALID."
                )

            Write-Log (
                "$DateString | INTEGRITY_FAILURE | " +
                "post-copy validation"
            )

            Remove-Item -LiteralPath $RawPath -Force -ErrorAction Stop`n`n            Write-Log "$DateString | INTEGRITY_FAILURE | post-copy validation | RAW_REMOVED"`n`n            return "INTEGRITY_FAILURE"
        }


        # ----------------------------------------------------
        # Independent comparison of pre/post properties.
        # ----------------------------------------------------

        if ($PreValidation.FileSizeBytes -ne
            $PostValidation.FileSizeBytes) {

            Add-ManifestRecord `
                -Date $Date `
                -Status "INTEGRITY_FAILURE" `
                -File $RawPath `
                -Validation "SIZE_MISMATCH" `
                -ErrorMessage (
                    "Taille pre-copy=" +
                    $PreValidation.FileSizeBytes +
                    " post-copy=" +
                    $PostValidation.FileSizeBytes
                )

            Write-Log (
                "$DateString | INTEGRITY_FAILURE | SIZE_MISMATCH"
            )

            return "INTEGRITY_FAILURE"
        }

        if ($PreValidation.Sha256 -ne
            $PostValidation.Sha256) {

            Add-ManifestRecord `
                -Date $Date `
                -Status "INTEGRITY_FAILURE" `
                -File $RawPath `
                -Validation "SHA256_MISMATCH" `
                -ErrorMessage (
                    "SHA-256 pre-copy=" +
                    $PreValidation.Sha256 +
                    " post-copy=" +
                    $PostValidation.Sha256
                )

            Write-Log (
                "$DateString | INTEGRITY_FAILURE | SHA256_MISMATCH"
            )

            return "INTEGRITY_FAILURE"
        }


        # ----------------------------------------------------
        # Final VALID manifest record.
        # ----------------------------------------------------

        Add-ManifestRecord `
            -Date $Date `
            -Status "VALID" `
            -File $RawPath `
            -FileSizeBytes $PostValidation.FileSizeBytes `
            -TickCount $PostValidation.TickCount `
            -Sha256 $PostValidation.Sha256 `
            -FirstTimestamp $PostValidation.FirstTimestamp `
            -LastTimestamp $PostValidation.LastTimestamp `
            -Validation $PostValidation.Validation

        Write-Log (
            "$DateString | VALID | " +
            "ticks=$($PostValidation.TickCount) | " +
            "sha256=$($PostValidation.Sha256)"
        )

        return "VALID"
    }
    catch {

        $Message = $_.Exception.Message

        Write-Log (
            "$DateString | FAILED | $Message"
        )

        Add-ManifestRecord `
            -Date $Date `
            -Status "FAILED" `
            -File "" `
            -Validation "EXCEPTION" `
            -ErrorMessage $Message

        return "FAILED"
    }
    finally {

        if (Test-Path -LiteralPath $TempRoot) {

            Remove-Item `
                -LiteralPath $TempRoot `
                -Recurse `
                -Force `
                -ErrorAction SilentlyContinue
        }
    }
}


# ============================================================
# 10. PROVENANCE
# ============================================================

$NodeVersion = "UNKNOWN"
try {
    $NodeVersion = (& node --version 2>$null).Trim()
    if ([string]::IsNullOrWhiteSpace($NodeVersion)) { throw "node --version returned empty output" }
}
catch {
    Write-Error "NODE_RUNTIME_UNAVAILABLE: $($_.Exception.Message)"
    exit 1
}

$Metadata = [ordered]@{
    run_id                  = $RunId
    run_start_utc           = $RunStartUtc
    runner                  = Split-Path `
                                -Leaf $RunnerResolved
    runner_sha256            = $RunnerHash
    instrument              = $Instrument
    timeframe               = $Timeframe
    volumes                 = $Volumes
    start_date               = $StartDate.ToString("yyyy-MM-dd")
    end_date_exclusive       = $EndDate.ToString("yyyy-MM-dd")
    node_version             = $NodeVersion
    dukascopy_node_version   = $DukascopyNodeVersion
    source                   = "Dukascopy"
    raw_root                 = $RawRoot
    manifest                 = $ManifestPath
    validation_schema        = $ExpectedColumns
    command_template         = (
        "npx dukascopy-node@1.50.0 " +
        "-i usatechidxusd -from YYYY-MM-DD " +
        "-to YYYY-MM-DD -t tick -f csv -v"
    )
}

$Metadata |
    ConvertTo-Json -Depth 10 |
    Set-Content `
        -LiteralPath $MetadataPath `
        -Encoding UTF8


# ============================================================
# 11. MAIN LOOP
# ============================================================

Write-Log "===== START DOWNLOAD V3.3 ====="
Write-Log "Run ID: $RunId"
Write-Log "Instrument: $Instrument"
Write-Log "Timeframe: $Timeframe"
Write-Log "Volumes: $Volumes"
Write-Log "Start: $($StartDate.ToString('yyyy-MM-dd'))"
Write-Log "End exclusive: $($EndDate.ToString('yyyy-MM-dd'))"
Write-Log "Dukascopy-node: $DukascopyNodeVersion"
Write-Log "Runner SHA256: $RunnerHash"


$Current = $StartDate

$Results = @()

while ($Current -lt $EndDate) {

    # --------------------------------------------------------
    # CRITICAL CONTROL-FLOW RULE:
    #
    # Process-Day owns all per-day branching.
    # The main loop ALWAYS advances the date here.
    # No continue/break exists inside Process-Day.
    # --------------------------------------------------------

    $Status = Process-Day -Date $Current

    $Results += [pscustomobject]@{
        Date   = $Current.ToString("yyyy-MM-dd")
        Status = $Status
    }

    $Next = $Current.AddDays(1)

    Write-Log (
        "$($Current.ToString('yyyy-MM-dd')) | " +
        "TERMINAL_STATUS=$Status | " +
        "NEXT_DATE=$($Next.ToString('yyyy-MM-dd'))"
    )

    $Current = $Next
}


# ============================================================
# 12. FINAL RUN SUMMARY
# ============================================================

$ValidCount = @(
    $Results |
    Where-Object { $_.Status -eq "VALID" }
).Count

$NoDataCount = @(
    $Results |
    Where-Object { $_.Status -eq "NO_DATA" }
).Count

$SkipCount = @(
    $Results |
    Where-Object { $_.Status -eq "SKIP" }
).Count

$FailedCount = @(
    $Results |
    Where-Object { $_.Status -eq "FAILED" }
).Count

$IntegrityFailureCount = @(
    $Results |
    Where-Object { $_.Status -eq "INTEGRITY_FAILURE" }
).Count

$BlockedCount = @(
    $Results |
    Where-Object { $_.Status -eq "BLOCKED" }
).Count


Write-Log "===== RUN SUMMARY ====="
Write-Log "VALID=$ValidCount"
Write-Log "NO_DATA=$NoDataCount"
Write-Log "SKIP=$SkipCount"
Write-Log "FAILED=$FailedCount"
Write-Log "INTEGRITY_FAILURE=$IntegrityFailureCount"
Write-Log "BLOCKED=$BlockedCount"


# ============================================================
# 13. GLOBAL PROCESS EXIT CODE
# ============================================================
#
# 0 = no serious failure
# 1 = FAILED / INTEGRITY_FAILURE / BLOCKED detected
#
# NO_DATA and SKIP are not failures.
# ============================================================

$SeriousFailureCount =
    $FailedCount +
    $IntegrityFailureCount +
    $BlockedCount

if ($SeriousFailureCount -gt 0) {

    Write-Log (
        "===== RUN RESULT: FAILURE ====="
    )

    exit 1
}

Write-Log "===== RUN RESULT: SUCCESS ====="

exit 0


