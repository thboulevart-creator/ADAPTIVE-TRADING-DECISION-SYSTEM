[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$SourceDirectory = (Join-Path $HOME 'Downloads')
)

$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot
$EvidenceRoot = Join-Path $RepoRoot 'LOCAL-EVIDENCE\dukascopy-trading-breaks-widget\2026-09-14'
$RawZipDirectory = Join-Path $EvidenceRoot 'raw-zips'
$ManifestPath = Join-Path $EvidenceRoot 'manifest-sha256.csv'

$ExpectedArtifacts = @(
    [pscustomobject]@{
        FileName    = 'dukascopy-trading-breaks-widget-2020-02-17-authoritative.zip'
        SHA256      = 'f49fb3aa5b66c22127eda3ac4593a387f6f83d3ab1d1d31eb742d44c49fb6a91'
        ArtifactId  = '10356927580'
        WorkflowRun = '34866241511'
        Role        = 'AUTHORITATIVE_CALIBRATION'
    },
    [pscustomobject]@{
        FileName    = 'dukascopy-trading-breaks-widget-2020-02-17-headed-browser.zip'
        SHA256      = 'aaf5341f3d7e10b60cc24622d6f16c2ffa3e3f31d6b108f69f53c6f3a2d48849'
        ArtifactId  = '10356971957'
        WorkflowRun = '34865846126'
        Role        = 'TECHNICAL_TRACE_NON_AUTHORITATIVE'
    },
    [pscustomobject]@{
        FileName    = 'dukascopy-trading-breaks-widget-pilot-2021-09-06-authoritative.zip'
        SHA256      = '8d8b568e17fd0e8d5d8c448742290313f78614ccd95c915aef5b978ed7f90ddc'
        ArtifactId  = '10357256669'
        WorkflowRun = '34866699952'
        Role        = 'AUTHORITATIVE_PILOT_PASS_A'
    }
)

New-Item -ItemType Directory -Path $RawZipDirectory -Force | Out-Null

foreach ($artifact in $ExpectedArtifacts) {
    $source = Join-Path $SourceDirectory $artifact.FileName
    $destination = Join-Path $RawZipDirectory $artifact.FileName

    if (Test-Path -LiteralPath $source) {
        $sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($sourceHash -ne $artifact.SHA256) {
            throw "SHA-256 mismatch for source '$source'. Expected $($artifact.SHA256), got $sourceHash. File was NOT moved."
        }

        if (Test-Path -LiteralPath $destination) {
            $destinationHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
            if ($destinationHash -ne $artifact.SHA256) {
                throw "Existing destination '$destination' has an unexpected SHA-256. Nothing was overwritten."
            }

            Remove-Item -LiteralPath $source -Force
            Write-Host "Already archived and verified: $($artifact.FileName)"
        }
        else {
            Move-Item -LiteralPath $source -Destination $destination
            Write-Host "Archived: $($artifact.FileName)"
        }
    }
    elseif (Test-Path -LiteralPath $destination) {
        $destinationHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($destinationHash -ne $artifact.SHA256) {
            throw "Existing destination '$destination' has an unexpected SHA-256."
        }
        Write-Host "Already archived and verified: $($artifact.FileName)"
    }
    else {
        throw "Missing expected ZIP '$($artifact.FileName)'. Download it first, then rerun this script. Expected source: $source"
    }
}

$manifestRows = foreach ($artifact in $ExpectedArtifacts) {
    $path = Join-Path $RawZipDirectory $artifact.FileName
    $item = Get-Item -LiteralPath $path
    $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()

    if ($hash -ne $artifact.SHA256) {
        throw "Post-archive SHA-256 mismatch for '$path'."
    }

    [pscustomobject]@{
        Filename         = $artifact.FileName
        SizeBytes        = $item.Length
        RelativePath     = "raw-zips/$($artifact.FileName)"
        LastWriteTimeUtc = $item.LastWriteTimeUtc.ToString('o')
        SHA256           = $hash
        Role             = $artifact.Role
        ArtifactId       = $artifact.ArtifactId
        WorkflowRun      = $artifact.WorkflowRun
    }
}

$manifestRows | Export-Csv -LiteralPath $ManifestPath -NoTypeInformation -Encoding UTF8

Write-Host ''
Write-Host 'Trading Breaks local evidence archive is complete.'
Write-Host "Raw ZIP directory: $RawZipDirectory"
Write-Host "Manifest:          $ManifestPath"
Write-Host ''
$manifestRows | Format-Table Filename, SizeBytes, SHA256, Role -AutoSize
