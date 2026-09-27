$ErrorActionPreference = "Stop"
$env:PYTHONDONTWRITEBYTECODE = "1"

param()

$Snapshot = "C:\Users\Boulevart\AppData\Local\ATDS\obsidian_projection\p5c3\snapshots\p5c3-open-snapshot-bf2b9a1e817b35abdb550375970f21f84fd65de56590abf925aec329b0468b3b.json"

if (Get-Process -Name "Obsidian" -ErrorAction SilentlyContinue) {
    throw "BLOCKED: close Obsidian completely before P5-C3R recovery."
}

Write-Host "=== P5-C3R RECOVERY CONTROL ===" -ForegroundColor Cyan
Write-Host "HEAD=$((git rev-parse HEAD).Trim())"

Write-Host "`n=== TARGETED TESTS ===" -ForegroundColor Cyan
python -B -m unittest `
    tests.obsidian_projection.test_obsidian_open_retry_contract_v0_1 `
    tests.obsidian_projection.test_obsidian_open_retry `
    tests.obsidian_projection.test_p5c3r_adversarial `
    -v
if ($LASTEXITCODE -ne 0) { throw "BLOCKED: P5-C3R targeted tests failed." }
Write-Host "P5C3R_TARGETED_TESTS=PASS" -ForegroundColor Green

Write-Host "`n=== FULL OBSIDIAN SUITE ===" -ForegroundColor Cyan
python -B -m unittest discover -s tests/obsidian_projection -p "test_*.py" -v
if ($LASTEXITCODE -ne 0) { throw "BLOCKED: full Obsidian suite failed." }
Write-Host "P5C3R_FULL_REBREAK=PASS" -ForegroundColor Green

git diff --quiet
if ($LASTEXITCODE -ne 0) { throw "BLOCKED: tracked files changed during tests." }
$Untracked = @(git ls-files --others --exclude-standard)
if ($Untracked.Count -ne 0) { throw "BLOCKED: unexpected untracked files: $($Untracked -join ', ')" }
Write-Host "CONTROL_CLONE_CLEAN=PASS" -ForegroundColor Green

Write-Host "`n=== SYNTHETIC WINDOWS LOCK BREAKER ===" -ForegroundColor Cyan
python -B -m tools.obsidian_projection.p5c3r_verify --synthetic-lock-breaker
if ($LASTEXITCODE -ne 0) { throw "BLOCKED: synthetic sharing-lock breaker failed." }
Write-Host "P5C3R_SYNTHETIC_LOCK_BREAKER=PASS" -ForegroundColor Green

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

Write-Host "`n=== RECOVER FAILED P5-C3 STATE ===" -ForegroundColor Cyan
python -B -m tools.obsidian_projection.p5c3r_verify --recover --snapshot "$Snapshot"
if ($LASTEXITCODE -ne 0) { throw "BLOCKED: P5-C3R recovery failed." }
Write-Host "P5C3R_RECOVERY=PASS" -ForegroundColor Green
