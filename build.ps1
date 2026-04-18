param(
    [string]$PythonExe,
    [switch]$SkipInstaller
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

$mainScript = Join-Path $repoRoot 'ytdlp_gui.py'
$versionFile = Join-Path $repoRoot 'windows-version-info.txt'
$installerScript = Join-Path $repoRoot 'installer.iss'

if (-not $PythonExe) {
    $venvPython = Join-Path $repoRoot '.venv\Scripts\python.exe'
    if (Test-Path $venvPython) {
        $PythonExe = $venvPython
    }
    else {
        $PythonExe = (Get-Command python -ErrorAction Stop).Source
    }
}

$portableExe = Join-Path $repoRoot 'dist\yt-dlp GUI.exe'
$installerOutput = Join-Path $repoRoot 'dist\installer'

Write-Host "Using Python: $PythonExe"
& $PythonExe -m pip install --upgrade pip
& $PythonExe -m pip install -r requirements-build.txt

& $PythonExe -m PyInstaller `
    --noconfirm `
    --clean `
    --specpath build `
    --windowed `
    --onefile `
    --name 'yt-dlp GUI' `
    --version-file $versionFile `
    $mainScript

if (-not (Test-Path $portableExe)) {
    throw "PyInstaller output was not created: $portableExe"
}

if ($SkipInstaller) {
    Write-Host "Portable build ready: $portableExe"
    exit 0
}

$isccCommand = Get-Command iscc.exe -ErrorAction SilentlyContinue
if (-not $isccCommand) {
    $isccCommand = Get-Command iscc -ErrorAction SilentlyContinue
}

if (-not $isccCommand) {
    $isccCandidates = @(
        'C:\Program Files (x86)\Inno Setup 6\ISCC.exe',
        'C:\Program Files\Inno Setup 6\ISCC.exe'
    )

    foreach ($candidate in $isccCandidates) {
        if (Test-Path $candidate) {
            $isccCommand = @{ Source = $candidate }
            break
        }
    }
}

if (-not $isccCommand) {
    Write-Warning 'Inno Setup Compiler (ISCC.exe) was not found. Portable .exe was built, but the installer was skipped.'
    Write-Host 'Install Inno Setup from https://jrsoftware.org/isinfo.php and run build.bat again.'
    exit 0
}

New-Item -ItemType Directory -Force -Path $installerOutput | Out-Null
& $isccCommand.Source '/DAppVersion=1.0.0' "/O$installerOutput" $installerScript

Write-Host "Installer build ready under: $installerOutput"