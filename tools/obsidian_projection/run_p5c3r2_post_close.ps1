param(
    [Parameter(Mandatory=$true)]
    [string]$Snapshot,
    [switch]$ManualVisualAccepted
)

$ErrorActionPreference = "Stop"
$env:PYTHONDONTWRITEBYTECODE = "1"

if (-not $ManualVisualAccepted) {
    throw "BLOCKED: manual visual acceptance flag missing."
}

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

Write-Host "=== P5-C3R2 POST-CLOSE VERIFY ===" -ForegroundColor Cyan
python -B -m tools.obsidian_projection.p5c3r2_verify `
    --post-close `
    --snapshot "$Snapshot" `
    --manual-visual-accepted

if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: P5-C3R2 post-close verification failed."
}

Write-Host "P5C3R2_POST_CLOSE=PASS" -ForegroundColor Green
