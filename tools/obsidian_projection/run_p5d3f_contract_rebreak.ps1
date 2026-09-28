$ErrorActionPreference = "Stop"

$ExpectedRepository = "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
$ExpectedContractBlob = "64744325251db350d26c0269090ce62d5fa5f2e8"
$ExpectedTestBlob = "6c7f3d5e1962132f4b609b637d176e67ccd376d5"

$ExternalPycache = Join-Path $env:TEMP "ATDS-P5D3F-CONTRACT-PYCACHE"
$OldPycachePrefix = $env:PYTHONPYCACHEPREFIX

Write-Host "=== P5-D3F PROMOTION HANDOFF CONTRACT RE-BREAK ===" -ForegroundColor Cyan
Write-Host "=== CONTRACT ONLY — NO HANDOFF RUNTIME / NO LIVE VAULT WRITE ===" -ForegroundColor Yellow

try {
    $Origin = (git remote get-url origin).Trim()

    $Normalized = $Origin
    if ($Normalized.StartsWith("git@github.com:")) {
        $Normalized = $Normalized.Substring("git@github.com:".Length)
    }
    elseif ($Normalized.StartsWith("https://github.com/")) {
        $Normalized = $Normalized.Substring("https://github.com/".Length)
    }
    elseif ($Normalized.StartsWith("ssh://git@github.com/")) {
        $Normalized = $Normalized.Substring("ssh://git@github.com/".Length)
    }
    else {
        throw "BLOCKED: unsupported origin form: $Origin"
    }

    if ($Normalized.EndsWith(".git")) {
        $Normalized = $Normalized.Substring(0, $Normalized.Length - 4)
    }

    $Normalized = $Normalized.Trim("/")

    if ($Normalized -ne $ExpectedRepository) {
        throw "BLOCKED: repository mismatch: $Normalized"
    }

    $Before = @(git status --porcelain --untracked-files=all)
    if ($Before.Count -ne 0) {
        throw "BLOCKED: working tree non propre avant P5-D3F contract re-break: $($Before -join ' | ')"
    }

    $ContractBlob = (git hash-object ".\tools\obsidian_projection\promotion_handoff_contract_v0_1.json").Trim()
    $TestBlob = (git hash-object ".\tests\obsidian_projection\test_promotion_handoff_contract_v0_1.py").Trim()

    if ($ContractBlob -ne $ExpectedContractBlob) {
        throw "BLOCKED: P5-D3F contract blob inattendu: $ContractBlob"
    }

    if ($TestBlob -ne $ExpectedTestBlob) {
        throw "BLOCKED: P5-D3F contract-test blob inattendu: $TestBlob"
    }

    Write-Host "P5D3F_CONTRACT_BLOB=PASS" -ForegroundColor Green
    Write-Host "P5D3F_CONTRACT_TEST_BLOB=PASS" -ForegroundColor Green

    if (Test-Path -LiteralPath $ExternalPycache) {
        Remove-Item -LiteralPath $ExternalPycache -Recurse -Force
    }

    New-Item -ItemType Directory -Path $ExternalPycache -Force | Out-Null
    $env:PYTHONPYCACHEPREFIX = $ExternalPycache

    python -m py_compile tests\obsidian_projection\test_promotion_handoff_contract_v0_1.py

    if ($LASTEXITCODE -ne 0) {
        throw "BLOCKED: P5-D3F contract test py_compile failed."
    }

    Write-Host "P5D3F_CONTRACT_PY_COMPILE=PASS" -ForegroundColor Green

    python -B -m unittest tests.obsidian_projection.test_promotion_handoff_contract_v0_1 -v

    if ($LASTEXITCODE -ne 0) {
        throw "BLOCKED: P5-D3F targeted contract tests failed."
    }

    Write-Host "P5D3F_CONTRACT_TARGETED=PASS" -ForegroundColor Green

    python -B -m unittest discover -s tests/obsidian_projection -p "test_*.py" -v

    if ($LASTEXITCODE -ne 0) {
        throw "BLOCKED: full Obsidian suite failed."
    }

    Write-Host "P5D3F_FULL_REBREAK=PASS" -ForegroundColor Green

    $After = @(git status --porcelain --untracked-files=all)
    if ($After.Count -ne 0) {
        throw "BLOCKED: working tree modifié après P5-D3F contract re-break: $($After -join ' | ')"
    }

    Write-Host "CONTROL_CLONE_CLEAN=PASS" -ForegroundColor Green
    Write-Host "P5D3F_CONTRACT_REBREAK_COMPLETED=PASS" -ForegroundColor Green
}
finally {
    if (Test-Path -LiteralPath $ExternalPycache) {
        Remove-Item -LiteralPath $ExternalPycache -Recurse -Force -ErrorAction SilentlyContinue
    }

    $env:PYTHONPYCACHEPREFIX = $OldPycachePrefix
}
