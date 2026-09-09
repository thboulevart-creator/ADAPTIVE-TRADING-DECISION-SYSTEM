[CmdletBinding()]
param(
    [string]$Symbol = "USATECHIDXUSD",
    [datetime]$StartDate = [datetime]::Parse("2025-01-01T00:00:00Z").ToUniversalTime(),
    [datetime]$EndDate = [datetime]::Parse("2025-12-31T23:00:00Z").ToUniversalTime(),
    [string]$OutputRoot = "data/raw/dukascopy",
    [int]$MaxRetries = 5,
    [int]$RetryDelaySeconds = 2,
    [int]$InterRequestDelaySeconds = 5,
    [int]$ServiceUnavailableBackoffSeconds = 10,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# IMPORTANT:
# - This script downloads Dukascopy's native hourly tick .bi5 files.
# - .bi5 files are retained exactly as received: no decompression, sorting,
#   deduplication, repair, filtering, resampling, or CSV conversion occurs here.
# - January is month 00 in the Dukascopy datafeed URL; December is month 11.
# - The local directory uses normal calendar month numbering (01..12).
# - Requests are deliberately paced to reduce transient 503 responses.
# - A 200 response with zero bytes is recorded as EMPTY_200 observation; it is
#   never promoted to DOWNLOADED and is not treated as a valid tick payload.

if ($EndDate -lt $StartDate) {
    throw "EndDate must be greater than or equal to StartDate."
}

if ($MaxRetries -lt 1) {
    throw "MaxRetries must be at least 1."
}

if ($RetryDelaySeconds -lt 0 -or $InterRequestDelaySeconds -lt 0 -or $ServiceUnavailableBackoffSeconds -lt 0) {
    throw "Delay parameters must be non-negative."
}

$StartDate = $StartDate.ToUniversalTime()
$EndDate = $EndDate.ToUniversalTime()
$Symbol = $Symbol.ToUpperInvariant()

$runId = [guid]::NewGuid().ToString("N")
$runStartedAt = [DateTime]::UtcNow
$symbolRoot = Join-Path $OutputRoot $Symbol
$manifestPath = Join-Path $symbolRoot "download-manifest-$runId.csv"
$logPath = Join-Path $symbolRoot "download-$runId.jsonl"

New-Item -ItemType Directory -Force -Path $symbolRoot | Out-Null

function Write-Log {
    param(
        [string]$Status,
        [string]$Url,
        [string]$Path,
        [long]$Bytes,
        [string]$Sha256,
        [int]$Attempts,
        [string]$ErrorMessage
    )

    $record = [ordered]@{
        run_id       = $runId
        recorded_at  = [DateTime]::UtcNow.ToString("o")
        symbol       = $Symbol
        status       = $Status
        url          = $Url
        path         = $Path
        bytes        = $Bytes
        sha256       = $Sha256
        attempts     = $Attempts
        error        = $ErrorMessage
    }

    ($record | ConvertTo-Json -Compress) | Add-Content -LiteralPath $logPath -Encoding UTF8
    [pscustomobject]$record | Export-Csv -LiteralPath $manifestPath -NoTypeInformation -Append -Encoding UTF8
}

function Get-StatusCodeFromException {
    param([System.Exception]$Exception)

    try {
        if ($null -ne $Exception.Response) {
            return [int]$Exception.Response.StatusCode.value__
        }
    }
    catch {
        # Status code unavailable; caller will record the exception text.
    }

    return 0
}

$downloaded = 0
$skippedExisting = 0
$empty200 = 0
$missing404 = 0
$failed = 0
$totalBytes = [int64]0

Write-Host "Dukascopy raw tick download"
Write-Host "Symbol : $Symbol"
Write-Host "Start  : $($StartDate.ToString('u'))"
Write-Host "End    : $($EndDate.ToString('u'))"
Write-Host "Output : $symbolRoot"
Write-Host "Run ID : $runId"
Write-Host "Manifest: $manifestPath"
Write-Host "Log     : $logPath"
Write-Host "Request delay : $InterRequestDelaySeconds second(s)"
Write-Host "503 backoff   : $ServiceUnavailableBackoffSeconds second(s) base"
Write-Host ""

$current = $StartDate.Date.AddHours($StartDate.Hour)
$last = $EndDate.Date.AddHours($EndDate.Hour)

while ($current -le $last) {
    # Dukascopy's URL uses zero-based months: Jan=00 ... Dec=11.
    $urlMonth = $current.Month - 1
    $url = "https://datafeed.dukascopy.com/datafeed/{0}/{1}/{2:00}/{3:00}/{4:00}h_ticks.bi5" -f `
        $Symbol, $current.Year, $urlMonth, $current.Day, $current.Hour

    $localDirectory = Join-Path $symbolRoot (Join-Path ([string]$current.Year) ("{0:00}" -f $current.Month))
    $localDirectory = Join-Path $localDirectory ("{0:00}" -f $current.Day)
    $localPath = Join-Path $localDirectory ("{0:00}h_ticks.bi5" -f $current.Hour)

    New-Item -ItemType Directory -Force -Path $localDirectory | Out-Null

    if ((Test-Path -LiteralPath $localPath) -and -not $Force) {
        $existingHash = (Get-FileHash -LiteralPath $localPath -Algorithm SHA256).Hash.ToLowerInvariant()
        $existingBytes = (Get-Item -LiteralPath $localPath).Length
        if ($existingBytes -gt 0) {
            $skippedExisting++
            $totalBytes += $existingBytes
            Write-Log -Status "SKIPPED_EXISTING" -Url $url -Path $localPath -Bytes $existingBytes -Sha256 $existingHash -Attempts 0 -ErrorMessage "Existing non-empty raw file retained; use -Force only for explicit replacement."
            if ($InterRequestDelaySeconds -gt 0) {
                Start-Sleep -Seconds $InterRequestDelaySeconds
            }
            $current = $current.AddHours(1)
            continue
        }
    }

    $success = $false
    $lastError = ""
    $attempts = 0

    for ($attempt = 1; $attempt -le $MaxRetries; $attempt++) {
        $attempts = $attempt
        $temporaryPath = "$localPath.part"

        try {
            if (Test-Path -LiteralPath $temporaryPath) {
                Remove-Item -LiteralPath $temporaryPath -Force
            }

            $response = Invoke-WebRequest -Uri $url -Method Get -UseBasicParsing -TimeoutSec 120
            $statusCode = [int]$response.StatusCode

            if ($statusCode -ne 200) {
                throw "HTTP status $statusCode"
            }

            if ($null -eq $response.RawContentStream) {
                throw "HTTP 200 response contained no raw content stream"
            }

            # Use the response byte stream so the downloaded binary .bi5 payload
            # is written without text decoding or transformation.
            $response.RawContentStream.Position = 0
            $fileStream = [System.IO.File]::Open($temporaryPath, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
            try {
                $response.RawContentStream.CopyTo($fileStream)
            }
            finally {
                $fileStream.Dispose()
            }

            $bytes = (Get-Item -LiteralPath $temporaryPath).Length
            if ($bytes -le 0) {
                # Preserve the source observation. Do not retry or promote it.
                $empty200++
                Remove-Item -LiteralPath $temporaryPath -Force -ErrorAction SilentlyContinue
                Write-Log -Status "EMPTY_200" -Url $url -Path $localPath -Bytes 0 -Sha256 "" -Attempts $attempt -ErrorMessage "HTTP 200 response produced an empty file; no tick payload was stored."
                Write-Host ("[{0}] EMPTY_200" -f $current.ToString("yyyy-MM-dd HH:mm"))
                $success = $true
                break
            }

            if (Test-Path -LiteralPath $localPath) {
                Remove-Item -LiteralPath $localPath -Force
            }
            Move-Item -LiteralPath $temporaryPath -Destination $localPath

            $sha256 = (Get-FileHash -LiteralPath $localPath -Algorithm SHA256).Hash.ToLowerInvariant()
            $downloaded++
            $totalBytes += $bytes
            Write-Log -Status "DOWNLOADED" -Url $url -Path $localPath -Bytes $bytes -Sha256 $sha256 -Attempts $attempt -ErrorMessage ""
            Write-Host ("[{0}] DOWNLOADED {1} bytes SHA256={2}" -f $current.ToString("yyyy-MM-dd HH:mm"), $bytes, $sha256)
            $success = $true
            break
        }
        catch {
            $lastError = $_.Exception.Message
            $statusCode = Get-StatusCodeFromException -Exception $_.Exception

            if (Test-Path -LiteralPath $temporaryPath) {
                Remove-Item -LiteralPath $temporaryPath -Force -ErrorAction SilentlyContinue
            }

            if ($statusCode -eq 404) {
                # A missing hour is a source observation, not a reason to
                # fabricate data. Record it and continue with the next hour.
                $missing404++
                Write-Log -Status "MISSING_404" -Url $url -Path $localPath -Bytes 0 -Sha256 "" -Attempts $attempt -ErrorMessage $lastError
                Write-Host ("[{0}] MISSING_404" -f $current.ToString("yyyy-MM-dd HH:mm"))
                $success = $true
                break
            }

            if ($attempt -lt $MaxRetries) {
                if ($statusCode -eq 503) {
                    $backoff = $ServiceUnavailableBackoffSeconds * [math]::Pow(2, $attempt - 1)
                    $retryNumber = $attempt + 1
                    Write-Host ("[{0}] HTTP 503; backoff {1} second(s) before retry {2}/{3}" -f $current.ToString("yyyy-MM-dd HH:mm"), $backoff, $retryNumber, $MaxRetries)
                    if ($backoff -gt 0) {
                        Start-Sleep -Seconds $backoff
                    }
                }
                elseif ($RetryDelaySeconds -gt 0) {
                    Start-Sleep -Seconds ($RetryDelaySeconds * $attempt)
                }
            }
        }
    }

    if (-not $success) {
        $failed++
        Write-Log -Status "FAILED" -Url $url -Path $localPath -Bytes 0 -Sha256 "" -Attempts $attempts -ErrorMessage $lastError
        Write-Host ("[{0}] FAILED after {1} attempt(s): {2}" -f $current.ToString("yyyy-MM-dd HH:mm"), $attempts, $lastError)
    }

    if ($InterRequestDelaySeconds -gt 0) {
        Start-Sleep -Seconds $InterRequestDelaySeconds
    }

    $current = $current.AddHours(1)
}

$runEndedAt = [DateTime]::UtcNow
$summary = [ordered]@{
    run_id             = $runId
    symbol             = $Symbol
    start_utc          = $StartDate.ToString("o")
    end_utc            = $EndDate.ToString("o")
    run_started_at_utc = $runStartedAt.ToString("o")
    run_ended_at_utc   = $runEndedAt.ToString("o")
    downloaded         = $downloaded
    skipped_existing   = $skippedExisting
    empty_200          = $empty200
    missing_404        = $missing404
    failed             = $failed
    total_bytes        = $totalBytes
    manifest           = $manifestPath
    log                = $logPath
    raw_only           = $true
    transformed        = $false
}

$summaryPath = Join-Path $symbolRoot "download-summary-$runId.json"
$summary | ConvertTo-Json | Set-Content -LiteralPath $summaryPath -Encoding UTF8

Write-Host ""
Write-Host "Completed."
Write-Host ($summary | ConvertTo-Json)
Write-Host "Summary: $summaryPath"

if ($failed -gt 0) {
    exit 2
}

exit 0
