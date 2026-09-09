[CmdletBinding()]
param(
    [string]$VenvPath = ".venv"
)

$ErrorActionPreference = "Stop"

$requiredMajor = 3
$requiredMinor = 13
$requirements = Join-Path $PSScriptRoot "..\requirements-mt5.txt"
$venv = Join-Path (Get-Location) $VenvPath

function Invoke-Python {
    param([string[]]$Arguments)
    & py @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Python launcher command failed with exit code $LASTEXITCODE."
    }
}

Write-Host "Python environment bootstrap for MT5 source discovery"
Write-Host "Required baseline: CPython $requiredMajor.$requiredMinor"

$py = Get-Command py -ErrorAction SilentlyContinue
if (-not $py) {
    throw "Python Launcher 'py' was not found. Install CPython $requiredMajor.$requiredMinor x64 first."
}

$version = & py -3.13 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
if ($LASTEXITCODE -ne 0) {
    throw "CPython $requiredMajor.$requiredMinor is not installed or is not accessible through the Python Launcher."
}

Write-Host "Detected CPython $version"

if (-not (Test-Path $venv)) {
    Write-Host "Creating isolated environment: $venv"
    Invoke-Python @("-3.13", "-m", "venv", $venv)
} else {
    Write-Host "Using existing isolated environment: $venv"
}

$venvPython = Join-Path $venv "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    throw "Expected virtual-environment interpreter not found: $venvPython"
}

& $venvPython -c "import sys; assert sys.version_info[:2] == (3,13), sys.version; print('venv:', sys.executable); print('python:', sys.version.split()[0])"
if ($LASTEXITCODE -ne 0) {
    throw "The isolated environment does not satisfy the Python 3.13 baseline."
}

Write-Host "Installing pinned MT5 dependency from $requirements"
& $venvPython -m pip install -r $requirements
if ($LASTEXITCODE -ne 0) {
    throw "Dependency installation failed."
}

Write-Host "Verifying dependency import"
& $venvPython -c "import MetaTrader5 as mt5; print('MetaTrader5:', mt5.__version__)"
if ($LASTEXITCODE -ne 0) {
    throw "MetaTrader5 import verification failed."
}

Write-Host "Environment bootstrap PASS"
Write-Host "Next: run tools\verify_python_environment.py with the venv interpreter."
