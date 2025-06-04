# README_bootstrap.md

## Overview

This repository provides **cross-platform bootstrap scripts** (`bootstrap_linux.sh`, `bootstrap_macos.sh`, `bootstrap_windows.ps1`) to automate the initial setup of developer environments on Linux, macOS, and Windows. The scripts handle system package manager installation, core tool setup, and environment preparation.

## Approach

- **Linux/macOS:**  
  Bash scripts install Homebrew (if needed), essential CLI tools, and Python.
- **Windows:**  
  PowerShell script installs [Chocolatey](https://chocolatey.org/) (the Windows package manager), then uses it to install core tools like Git, VS Code, Python, and Just.

## Environments Supported

| OS         | Script                | Package Manager | Shell         | Permissions Needed      |
|------------|-----------------------|-----------------|---------------|------------------------|
| Linux      | `sh/bootstrap_linux.sh` | apt + Homebrew  | Bash          | sudo (admin)           |
| macOS      | `sh/bootstrap_macos.sh` | Homebrew        | Bash/zsh      | sudo (admin)           |
| Windows    | `sh/bootstrap_windows.ps1` | Chocolatey      | PowerShell    | Administrator required |

## Permissions & Requirements

### Windows (Chocolatey)
- **Run PowerShell as Administrator** (see below)
- **PowerShell v3+** (v5+ recommended)
- **.NET Framework 4.8+** (installer will prompt if missing)
- **Execution Policy:**  
  - Run `Get-ExecutionPolicy`  
  - If `Restricted`, run `Set-ExecutionPolicy Bypass -Scope Process` or `Set-ExecutionPolicy AllSigned`[1][3][5][6][7]

### Linux/macOS (Homebrew)
- **sudo/admin access** for installing system packages
- **Internet connection** for downloading scripts and packages

## How to Run

### Windows

1. Open PowerShell as Administrator:
   - Right-click Start > Windows Terminal (Admin) or search for PowerShell, right-click, "Run as Administrator"[5][7].
2. Set execution policy if needed:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process
   ```
3. Run the bootstrap script:
   ```powershell
   .\sh\bootstrap_windows.ps1
   ```

### Linux/macOS

```bash
chmod +x sh/bootstrap_linux.sh
./sh/bootstrap_linux.sh
```
or
```bash
chmod +x sh/bootstrap_macos.sh
./sh/bootstrap_macos.sh
```

## Azure Infrastructure Context

- **VMs:**  
  Use these scripts in Azure VM custom script extensions or as part of initialisation for Linux/Windows VMs.
- **DevOps Pipelines:**  
  Integrate as steps in Azure DevOps pipelines to provision build/test agents.
- **Azure Cloud Shell:**  
  For Linux-based agents, run the bootstrap script directly; for Windows-based agents, use the PowerShell script.
- **Permissions:**  
  Ensure VM or agent has administrator/sudo rights to install system packages.

## References

[1]: https://chocolatey.org/install  
[2]: https://docs.chocolatey.org/en-us/choco/setup/  
[3]: https://www.liquidweb.com/blog/how-to-install-chocolatey-on-windows/  
[5]: https://github.com/Vets-Who-Code/windows-dev-guide  
[6]: https://github.com/berkanuslu/choco-development-enviroment-setup  
[7]: https://www.xda-developers.com/simplify-pc-set-up-with-chocolatey-package-manager/

