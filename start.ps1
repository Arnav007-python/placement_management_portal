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

$Port = if ($env:PORT) { $env:PORT } else { "5000" }
$LanIp = (
    Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
        Where-Object {
            $_.IPAddress -notlike "127.*" -and
            $_.IPAddress -notlike "169.254.*" -and
            $_.PrefixOrigin -ne "WellKnown"
        } |
        Select-Object -First 1 -ExpandProperty IPAddress
)

Write-Host ""
Write-Host "Placement Portal is starting."
Write-Host "This laptop: http://127.0.0.1:$Port"
if ($LanIp) {
    Write-Host "Other laptops / mobile phones on the same Wi-Fi: http://$LanIp`:$Port"
} else {
    Write-Host "Could not detect a Wi-Fi/LAN IP address. Run ipconfig and use your IPv4 address with port $Port."
}
Write-Host "Keep this terminal open while showing the project."
Write-Host ""
$env:HOST = "0.0.0.0"
$env:PORT = $Port
& $AppPython run.py
