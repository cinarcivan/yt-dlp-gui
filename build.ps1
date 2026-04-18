param(
    [string]$PythonExe,
    [string]$AppVersion,
    [switch]$SkipInstaller
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

$versionSource = Join-Path $repoRoot 'app_version.py'
$mainScript = Join-Path $repoRoot 'ytdlp_gui.py'
$installerScript = Join-Path $repoRoot 'installer.iss'

if (-not $AppVersion) {
        $versionMatch = Select-String -Path $versionSource -Pattern 'APP_VERSION\s*=\s*"([^"]+)"'
        if (-not $versionMatch) {
                throw 'APP_VERSION could not be read from app_version.py'
        }
        $AppVersion = $versionMatch.Matches[0].Groups[1].Value
}

$numericVersion = ($AppVersion -replace '[^0-9\.]', '').Trim('.')
if (-not $numericVersion) {
        throw "Invalid AppVersion: $AppVersion"
}

$versionParts = $numericVersion.Split('.')
while ($versionParts.Count -lt 4) {
        $versionParts += '0'
}
$versionParts = $versionParts[0..3]
$versionTuple = $versionParts -join ', '

$generatedVersionFile = Join-Path $repoRoot 'build\windows-version-info.txt'
New-Item -ItemType Directory -Force -Path (Split-Path $generatedVersionFile -Parent) | Out-Null
@"
VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=($versionTuple),
        prodvers=($versionTuple),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',
                    [
                        StringStruct('CompanyName', 'Cinar Civan'),
                        StringStruct('FileDescription', 'yt-dlp GUI'),
                        StringStruct('FileVersion', '$AppVersion'),
                        StringStruct('InternalName', 'yt-dlp GUI'),
                        StringStruct('OriginalFilename', 'yt-dlp GUI.exe'),
                        StringStruct('ProductName', 'yt-dlp GUI'),
                        StringStruct('ProductVersion', '$AppVersion')
                    ]
                )
            ]
        ),
        VarFileInfo([VarStruct('Translation', [1033, 1200])])
    ]
)
"@ | Set-Content -Path $generatedVersionFile -Encoding ASCII

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
Write-Host "App version: $AppVersion"
& $PythonExe -m pip install --upgrade pip
& $PythonExe -m pip install -r requirements-build.txt

& $PythonExe -m PyInstaller `
    --noconfirm `
    --clean `
    --specpath build `
    --windowed `
    --onefile `
    --name 'yt-dlp GUI' `
    --version-file $generatedVersionFile `
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
& $isccCommand.Source "/DAppVersion=$AppVersion" "/O$installerOutput" $installerScript

Write-Host "Installer build ready under: $installerOutput"