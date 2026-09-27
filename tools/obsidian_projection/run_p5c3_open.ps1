param(
    [Parameter(Mandatory=$true)]
    [string]$Snapshot
)

$ErrorActionPreference = "Stop"
$env:PYTHONDONTWRITEBYTECODE = "1"

if (-not (Test-Path -LiteralPath $Snapshot)) {
    throw "BLOCKED: P5-C3 snapshot missing."
}

Write-Host "=== P5-C3 OBSIDIAN-OPEN EXPERIMENT ===" -ForegroundColor Cyan
python -B -m tools.obsidian_projection.p5c3_verify `
    --run-open `
    --snapshot "$Snapshot"

if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: P5-C3 open experiment failed."
}

Write-Host "`nP5C3_OPEN_EXPERIMENT_EXECUTION_COMPLETE" -ForegroundColor Green
Write-Host "Keep Obsidian open and capture CURRENT.md for manual visual acceptance."
