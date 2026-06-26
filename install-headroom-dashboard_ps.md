#!/usr/bin/env pwsh
[CmdletBinding()]
param(
    [string]$HeadroomRef = $env:HEADROOM_REF,
    [string]$HeadroomExtras = $env:HEADROOM_EXTRAS,
    [string]$HeadroomHome = $env:HEADROOM_HOME,
    [string]$HeadroomVenv = $env:HEADROOM_VENV,
    [string]$HeadroomUserBin = $env:HEADROOM_USER_BIN,
    [string]$HeadroomTelemetry = $env:HEADROOM_TELEMETRY,
    [int]$HeadroomPort = $(if ($env:HEADROOM_PORT) { [int]$env:HEADROOM_PORT } else { 8787 })
)

$ErrorActionPreference = "Stop"

$isWindowsPlatform = ($PSVersionTable.PSEdition -eq "Desktop") -or ($env:OS -eq "Windows_NT")

if ([string]::IsNullOrWhiteSpace($HeadroomRef)) {
    $HeadroomRef = "main"
}

if ([string]::IsNullOrWhiteSpace($HeadroomExtras)) {
    $HeadroomExtras = "all"
}

if ([string]::IsNullOrWhiteSpace($HeadroomHome)) {
    $HeadroomHome = Join-Path $HOME ".headroom"
}

if ([string]::IsNullOrWhiteSpace($HeadroomVenv)) {
    $HeadroomVenv = Join-Path $HeadroomHome "venv"
}

if ([string]::IsNullOrWhiteSpace($HeadroomTelemetry)) {
    $HeadroomTelemetry = "on"
}

$python = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python -ErrorAction SilentlyContinue
}

if (-not $python) {
    throw "python3 or python is required."
}

$pythonExe = $python.Source

$pythonVersion = & $pythonExe -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
& $pythonExe -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 'Error: Headroom requires Python 3.10+.')"

$userBin = $HeadroomUserBin
if ([string]::IsNullOrWhiteSpace($userBin)) {
    $userBin = & $pythonExe -c "import site, pathlib; print(pathlib.Path(site.USER_BASE) / ('Scripts' if __import__('os').name == 'nt' else 'bin'))"
}
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($userBin)) {
    if ($isWindowsPlatform) {
        $userBin = Join-Path $env:APPDATA "Python/Scripts"
    } else {
        $userBin = Join-Path $HOME ".local/bin"
    }
}

if ([string]::IsNullOrWhiteSpace($userBin)) {
    throw "Could not resolve user script directory. Set HEADROOM_USER_BIN and retry."
}

$venvPython = if ($isWindowsPlatform) {
    Join-Path $HeadroomVenv "Scripts/python.exe"
} else {
    Join-Path $HeadroomVenv "bin/python"
}

$venvHeadroom = if ($isWindowsPlatform) {
    Join-Path $HeadroomVenv "Scripts/headroom.exe"
} else {
    Join-Path $HeadroomVenv "bin/headroom"
}

Write-Host "Installing Headroom into: $HeadroomVenv"
New-Item -ItemType Directory -Force -Path $HeadroomHome, $userBin | Out-Null

& $pythonExe -m venv $HeadroomVenv
& $venvPython -m pip install --upgrade pip wheel setuptools
& $venvPython -m pip install --upgrade --no-cache-dir "headroom-ai[$HeadroomExtras] @ git+https://github.com/headroomlabs-ai/headroom.git@$HeadroomRef"

$certFile = & $venvPython -c "import certifi; print(certifi.where())"

$wrapperPath = if ($isWindowsPlatform) {
    Join-Path $userBin "headroom.ps1"
} else {
    Join-Path $userBin "headroom"
}

if ($isWindowsPlatform) {
    @"
`$ErrorActionPreference = "Stop"
`$env:SSL_CERT_FILE = "$certFile"
`$env:REQUESTS_CA_BUNDLE = `$env:SSL_CERT_FILE
& "$venvHeadroom" @args
exit `$LASTEXITCODE
"@ | Set-Content -Path $wrapperPath -Encoding UTF8
} else {
    @"
#!/usr/bin/env bash
set -euo pipefail

export SSL_CERT_FILE="$certFile"
export REQUESTS_CA_BUNDLE="`$SSL_CERT_FILE"

exec "$venvHeadroom" "`$@"
"@ | Set-Content -Path $wrapperPath -Encoding UTF8
    chmod +x $wrapperPath
}

Write-Host ""
Write-Host "Installed wrapper: $wrapperPath"
Write-Host "Headroom version:"
& $wrapperPath --version

Write-Host ""
Write-Host "Checking dashboard command:"
& $wrapperPath dashboard --help | Out-Null
Write-Host "OK: headroom dashboard is available."

Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Make sure this is on PATH before other Python script dirs:"
Write-Host "     `$env:PATH = `"$userBin$([IO.Path]::PathSeparator)`$env:PATH`""
Write-Host ""
Write-Host "  2. Start the proxy:"
Write-Host "     `$env:HEADROOM_TELEMETRY = `"$HeadroomTelemetry`""
Write-Host "     headroom proxy --port $HeadroomPort --memory --code-aware --telemetry"
Write-Host ""
Write-Host "  3. Open the dashboard:"
Write-Host "     headroom dashboard"
Write-Host "     # or: http://127.0.0.1:$HeadroomPort/dashboard"
Write-Host ""
Write-Host "For a custom OpenAI-compatible gateway upstream:"
Write-Host "     `$env:OPENAI_TARGET_API_URL = `"https://your-gateway.example.com`""
Write-Host "     `$env:HEADROOM_TELEMETRY = `"$HeadroomTelemetry`""
Write-Host "     headroom proxy --port $HeadroomPort --memory --code-aware --telemetry"
