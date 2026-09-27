param(
    [Parameter(Mandatory=$true)]
    [string]$Snapshot
)

$ErrorActionPreference = "Stop"
$env:PYTHONDONTWRITEBYTECODE = "1"

Write-Host "=== P5-C3 OBSERVED OPEN CONTROL ===" -ForegroundColor Cyan
Write-Host "HEAD=$((git rev-parse HEAD).Trim())"

Write-Host "`n=== TARGETED TESTS ===" -ForegroundColor Cyan
python -B -m unittest `
    tests.obsidian_projection.test_obsidian_open_compatibility_contract_v0_1 `
    tests.obsidian_projection.test_obsidian_open_compatibility `
    tests.obsidian_projection.test_p5c3_adversarial `
    -v

if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: P5-C3 targeted tests failed."
}

Write-Host "P5C3_TARGETED_TESTS=PASS" -ForegroundColor Green

Write-Host "`n=== FULL OBSIDIAN SUITE ===" -ForegroundColor Cyan
python -B -m unittest discover `
    -s tests/obsidian_projection `
    -p "test_*.py" `
    -v

if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: full Obsidian suite failed."
}

Write-Host "P5C3_FULL_REBREAK=PASS" -ForegroundColor Green

git diff --quiet
if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: tracked files changed during tests."
}

$Untracked = @(git ls-files --others --exclude-standard)
if ($Untracked.Count -ne 0) {
    throw "BLOCKED: unexpected untracked files: $($Untracked -join ', ')"
}

Write-Host "CONTROL_CLONE_CLEAN=PASS" -ForegroundColor Green

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

Write-Host "`n=== READ-ONLY OPEN DIAGNOSTIC ===" -ForegroundColor Cyan
python -B -m tools.obsidian_projection.p5c3_verify `
    --diagnose-open `
    --snapshot "$Snapshot"

if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: P5-C3 read-only diagnostic failed."
}

Write-Host "P5C3_OPEN_DIAGNOSTIC=PASS" -ForegroundColor Green

Write-Host "`n=== INSTRUMENTED RUN-OPEN ===" -ForegroundColor Cyan
python -B -m tools.obsidian_projection.p5c3_verify `
    --run-open `
    --snapshot "$Snapshot"

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nP5C3_RUN_OPEN=FAIL_OR_BLOCKED" -ForegroundColor Yellow
    exit 2
}

Write-Host "`nP5C3_RUN_OPEN=PASS" -ForegroundColor Green
