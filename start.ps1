$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$RunEnvPython = Join-Path $ProjectRoot "runenv\Scripts\python.exe"
$BundledPython = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$AppPython = $VenvPython

Set-Location $ProjectRoot

function Test-PythonPackage {
    param(
        [string]$PythonPath,
        [string]$PackageName
    )

    if (-not (Test-Path $PythonPath)) {
        return $false
    }

    $PreviousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $PythonPath -c "import $PackageName" 1>$null 2>$null
    $PackageExitCode = $LASTEXITCODE
    $ErrorActionPreference = $PreviousErrorActionPreference
    return $PackageExitCode -eq 0
}

function Get-BasePython {
    if (Test-Path $RunEnvPython) {
        return $RunEnvPython
    }
    if (Test-Path $BundledPython) {
        return $BundledPython
    }
    $PythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($PythonCommand) {
        return $PythonCommand.Source
    }
    $PyCommand = Get-Command py -ErrorAction SilentlyContinue
    if ($PyCommand) {
        return $PyCommand.Source
    }
    throw "Python was not found. Install Python 3.11+ or run this from an environment where python is available."
}

if (Test-PythonPackage -PythonPath $RunEnvPython -PackageName "flask") {
    $AppPython = $RunEnvPython
}

if ($AppPython -eq $VenvPython -and (Test-Path $VenvPython)) {
    $PreviousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $VenvPython -c "import sys; print(sys.executable)" 1>$null 2>$null
    $VenvExitCode = $LASTEXITCODE
    $ErrorActionPreference = $PreviousErrorActionPreference
    if ($VenvExitCode -ne 0) {
        Write-Host "Existing virtual environment is not usable. Recreating it..."
        Remove-Item -LiteralPath (Join-Path $ProjectRoot ".venv") -Recurse -Force
    }
}

if ($AppPython -eq $VenvPython -and -not (Test-Path $VenvPython)) {
    Write-Host "Creating virtual environment..."
    $BasePython = Get-BasePython
    & $BasePython -m venv .venv
}

if ($AppPython -eq $VenvPython) {
    Write-Host "Installing requirements..."
    & $VenvPython -m pip install -r requirements.txt
}

Write-Host "Preparing demo database..."
& $AppPython -c "from app import create_app; from app.bootstrap import ensure_admin_account; app=create_app(); ctx=app.app_context(); ctx.push(); ensure_admin_account(); print('Admin account is ready.')"

Write-Host ""
Write-Host "Placement Portal is starting at http://127.0.0.1:5000"
Write-Host "Keep this terminal open while showing the project."
Write-Host ""
& $AppPython run.py
