$ErrorActionPreference = "Stop"

$Sandbox = "C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C3-OBSIDIAN-OPEN-SANDBOX"
$Evidence = "C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-P5C3-CONTROL-EVIDENCE"
$LocalState = Join-Path $env:LOCALAPPDATA "ATDS\obsidian_projection\p5c3"
$LiveVault = "C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION"

if (Get-Process -Name "Obsidian" -ErrorAction SilentlyContinue) {
    throw "BLOCKED: close Obsidian completely before P5-C3 reset."
}

if ($Sandbox -eq $LiveVault -or $Evidence -eq $LiveVault) {
    throw "BLOCKED: reset path overlaps real Vault."
}

if (Test-Path -LiteralPath $Sandbox) {
    $Required = @(
        (Join-Path $Sandbox "CURRENT.md"),
        (Join-Path $Sandbox "generations\GEN_A"),
        (Join-Path $Sandbox "generations\GEN_B"),
        (Join-Path $Sandbox ".obsidian")
    )
    foreach ($Item in $Required) {
        if (-not (Test-Path -LiteralPath $Item)) {
            throw "BLOCKED: sandbox identity check failed: $Item"
        }
    }
    Remove-Item -LiteralPath $Sandbox -Recurse -Force
}

if (Test-Path -LiteralPath $Evidence) {
    Remove-Item -LiteralPath $Evidence -Recurse -Force
}

if (Test-Path -LiteralPath $LocalState) {
    Remove-Item -LiteralPath $LocalState -Recurse -Force
}

if (Test-Path -LiteralPath $LiveVault) {
    Write-Host "REAL_VAULT_PRESERVED=PASS" -ForegroundColor Green
} else {
    throw "BLOCKED: real Vault unexpectedly missing after reset."
}

Write-Host "P5C3_RESET=PASS" -ForegroundColor Green
