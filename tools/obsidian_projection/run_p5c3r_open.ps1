param(
    [Parameter(Mandatory=$true)]
    [string]$Snapshot
)

$ErrorActionPreference = "Stop"
$env:PYTHONDONTWRITEBYTECODE = "1"

if (-not (Test-Path -LiteralPath $Snapshot)) {
    $Leaf = Split-Path -Leaf $Snapshot
    $BackupRoot = "C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C3-CONTROL-EVIDENCE\snapshots"
    $Backup = Join-Path $BackupRoot $Leaf
    if (Test-Path -LiteralPath $Backup) {
        Write-Host "SNAPSHOT_FALLBACK=ONEDRIVE_CONTROL_COPY" -ForegroundColor Yellow
        $Snapshot = $Backup
    } else {
        throw "BLOCKED: both P5-C3 snapshot copies are missing."
    }
}

Write-Host "=== P5-C3R READ-ONLY PRECHECK ===" -ForegroundColor Cyan
python -B -m tools.obsidian_projection.p5c3_verify --diagnose-open --snapshot "$Snapshot"
if ($LASTEXITCODE -ne 0) { throw "BLOCKED: read-only open diagnostic failed." }

Write-Host "`n=== P5-C3R RETRY OPEN EXPERIMENT ===" -ForegroundColor Cyan
python -B -m tools.obsidian_projection.p5c3r_verify --run-open --snapshot "$Snapshot"
if ($LASTEXITCODE -ne 0) {
    Write-Host "P5C3R_RUN_OPEN=FAIL_OR_BLOCKED" -ForegroundColor Yellow
    exit 2
}
Write-Host "P5C3R_RUN_OPEN=PASS" -ForegroundColor Green
