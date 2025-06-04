# Bootstrap Windows dev machine with Chocolatey and core tools

# Ensure running as Administrator
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Please run this script as Administrator!"
    exit 1
}

# Install Chocolatey if missing
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
} else {
    Write-Host "Chocolatey already installed."
}

# List of core packages to install
$packages = @(
    "git",
    "vscode",
    "googlechrome",
    "7zip",
    "python",
    "just"         # Just is available on Chocolatey!
)

foreach ($pkg in $packages) {
    Write-Host "Installing $pkg..."
    choco install $pkg -y --no-progress
}
