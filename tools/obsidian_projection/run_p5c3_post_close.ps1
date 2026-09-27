param(
    [Parameter(Mandatory=$true)]
    [string]$Snapshot,

    [switch]$ManualVisualAccepted
)

$ErrorActionPreference = "Stop"
$env:PYTHONDONTWRITEBYTECODE = "1"

if (-not (Test-Path -LiteralPath $Snapshot)) {
    throw "BLOCKED: P5-C3 snapshot missing."
}

if (-not $ManualVisualAccepted) {
    throw "BLOCKED: manual visual acceptance flag missing."
}

Write-Host "=== P5-C3 POST-CLOSE VERIFY ===" -ForegroundColor Cyan
python -B -m tools.obsidian_projection.p5c3_verify `
    --post-close `
    --snapshot "$Snapshot" `
    --manual-visual-accepted

if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: P5-C3 post-close verification failed."
}

Write-Host "`nP5C3_POST_CLOSE_EXECUTION_PASS" -ForegroundColor Green
