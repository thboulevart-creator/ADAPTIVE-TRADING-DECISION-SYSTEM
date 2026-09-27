$ErrorActionPreference = "Stop"

$env:PYTHONDONTWRITEBYTECODE = "1"

Write-Host "=== P5-C3 CONTROL + PREPARE ===" -ForegroundColor Cyan
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

Write-Host "`n=== P5-C3 PREPARE ===" -ForegroundColor Cyan
python -B -m tools.obsidian_projection.p5c3_verify --prepare

if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: P5-C3 prepare failed."
}

Write-Host "`nP5C3_PREPARE_EXECUTION_COMPLETE" -ForegroundColor Green
Write-Host "Do not delete the control clone or sandbox yet."
