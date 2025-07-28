# setup_build_tools.ps1

# 0. Ensure script stops on any error
$ErrorActionPreference = 'Stop'

# 1. Install Chocolatey if missing
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..." -ForegroundColor Cyan
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# 2. Refresh environment to pick up choco
& cmd /c "refreshenv" | Out-Null

# 3. Install Visual Studio 2022 Build Tools + C++ workload
Write-Host "Installing Visual Studio 2022 Build Tools + vctools workload..." -ForegroundColor Cyan
choco install visualstudio2022buildtools `
    --includeRecommended `
    --package-parameters "--add Microsoft.VisualStudio.Workload.VCTools" `
    --no-progress -y

# 4. Ensure the vctools workload is present (in case separate)
Write-Host "Installing vctools workload explicitly..." -ForegroundColor Cyan
choco install visualstudio2022-workload-vctools --no-progress -y

# 5. Install CMake silently and add to PATH
Write-Host "Installing CMake..." -ForegroundColor Cyan
choco install cmake --install-arguments "'ADD_CMAKE_TO_PATH=System'" --no-progress -y

# 6. Open a Native Tools command prompt to register environment variables
#    This step ensures nmake, cl.exe, and all MSVC tools are on your current PATH.
Write-Host "Initializing Native Tools environment for this session..." -ForegroundColor Cyan
& cmd /c '"%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat"' `
    -NoLogo | Out-Null

# 7. Verify tools
Write-Host "`nVerifying installations:" -ForegroundColor Green
Write-Host " cl.exe version:" -ForegroundColor Yellow
cl.exe
Write-Host "`n nmake version:" -ForegroundColor Yellow
nmake /?
Write-Host "`n cmake version:" -ForegroundColor Yellow
cmake --version

Write-Host "`nAll build tools installed successfully!" -ForegroundColor Green
