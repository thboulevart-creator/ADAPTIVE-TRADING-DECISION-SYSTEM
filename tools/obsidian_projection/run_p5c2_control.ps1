$ErrorActionPreference = "Stop"

$Repo = (Get-Location).Path

if (-not (Test-Path -LiteralPath (Join-Path $Repo ".git"))) {
    throw "BLOCKED: run from the root of the P5-C2 control clone."
}

$env:PYTHONDONTWRITEBYTECODE = "1"

Write-Host "=== P5-C2 CONTROL ===" -ForegroundColor Cyan
Write-Host "HEAD=$((git rev-parse HEAD).Trim())"

Write-Host "`n=== TARGETED TESTS ===" -ForegroundColor Cyan
python -B -m unittest `
    tests.obsidian_projection.test_promotion_experiment `
    tests.obsidian_projection.test_p5c2_adversarial `
    -v

if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: P5-C2 targeted tests failed."
}

Write-Host "P5C2_TARGETED_TESTS=PASS" -ForegroundColor Green

Write-Host "`n=== FULL OBSIDIAN SUITE ===" -ForegroundColor Cyan
python -B -m unittest discover `
    -s tests/obsidian_projection `
    -p "test_*.py" `
    -v

if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: full Obsidian suite failed."
}

Write-Host "P5C2_FULL_REBREAK=PASS" -ForegroundColor Green

git diff --quiet
if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: tracked files changed during tests."
}

$Untracked = @(git ls-files --others --exclude-standard)
if ($Untracked.Count -ne 0) {
    throw "BLOCKED: unexpected untracked files: $($Untracked -join ', ')"
}

Write-Host "CONTROL_CLONE_CLEAN=PASS" -ForegroundColor Green

Write-Host "`n=== P5-C2 PREFLIGHT ===" -ForegroundColor Cyan
python -B -m tools.obsidian_projection.p5c2_verify --preflight

if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: P5-C2 preflight failed."
}

Write-Host "P5C2_PREFLIGHT=PASS" -ForegroundColor Green

Write-Host "`n=== P5-C2 SANDBOX EXPERIMENT ===" -ForegroundColor Cyan
Write-Host "This phase may take several minutes."

python -B -m tools.obsidian_projection.p5c2_verify --run-experiment

if ($LASTEXITCODE -ne 0) {
    throw "BLOCKED: P5-C2 experiment did not qualify a filesystem candidate."
}

Write-Host "`nP5C2_EXPERIMENT_EXECUTION_PASS" -ForegroundColor Green
Write-Host "IMPORTANT: sandbox is intentionally preserved for evidence."
