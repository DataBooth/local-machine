# `local-machine`

Shell scripts and [justfile](https://github.com/casey/just) recipes for setting up and configuring macOS, Linux, and Windows machines for data science and engineering.


- [`local-machine`](#local-machine)
  - [Features](#features)
  - [Quick Start](#quick-start)
    - [1. Clone this repository](#1-clone-this-repository)
    - [2. Bootstrap your machine (first time only)](#2-bootstrap-your-machine-first-time-only)
      - [macOS](#macos)
      - [Linux](#linux)
      - [Windows](#windows)
    - [3. Run setup recipes](#3-run-setup-recipes)
  - [Structure](#structure)
  - [Customisation](#customisation)
  - [Requirements](#requirements)
  - [Environments \& Permissions](#environments--permissions)
  - [Why use this?](#why-use-this)
  - [Future Plans](#future-plans)
  - [Appendix: Azure Infrastructure Context](#appendix-azure-infrastructure-context)
  - [Appendix: Xcode Command Line Tools (macOS only)](#appendix-xcode-command-line-tools-macos-only)


---

## Features

- **Automated setup** for Mac, Linux, and Windows developer environments
- Modular, repeatable setup using just
- Installs Homebrew (Mac/Linux), Chocolatey (Windows), and core CLI tools
- Creates standard code/data directories with documentation
- Easily customisable for your own stack

---

## Quick Start

### 1. Clone this repository

```sh
git clone https://github.com/DataBooth/local-machine.git
cd local-machine
```

### 2. Bootstrap your machine (first time only)

#### macOS 

This script installs Xcode Command Line Tools, Homebrew, and `just` if they are not already present.

```sh
chmod +x sh/bootstrap_macos.sh
./sh/bootstrap_macos.sh
```

#### Linux

```sh
chmod +x sh/bootstrap_linux.sh
./sh/bootstrap_linux.sh
```

*Note: On Linux in Docker, see the [Dockerfile](Dockerfile) example for a robust Homebrew install method.*

#### Windows

Open PowerShell as Administrator and run:

```powershell
Set-ExecutionPolicy Bypass -Scope Process
.\sh\bootstrap_windows.ps1
```

This installs [Chocolatey](https://chocolatey.org) and core tools.

### 3. Run setup recipes

After bootstrapping, use the `just` command to run modular setup steps.

- To run all setup steps:
  ```sh
  just all
  ```
- Or run individual steps, e.g.:
  ```sh
  just vscode
  just iterm2
  just pipx
  ```

See the appropriate `justfile` for your OS: [justfile.macos](just/justfile.macos), [justfile.linux](just/justfile.linux), [justfile.windows](just/justfile.windows) for all available recipes.

---

## Structure

- `sh/bootstrap_macos.sh` – Bootstraps macOS with Xcode tools, Homebrew, and just.
- `sh/bootstrap_linux.sh` – Bootstraps Linux with Homebrew and just (see Dockerfile for robust approach).
- `sh/bootstrap_windows.ps1` – Bootstraps Windows with Chocolatey and just.
- `just/justfile.macos`, `just/justfile.linux`, `just/justfile.windows` – Modular, repeatable setup recipes.
- Additional shell scripts or configuration files as needed.

---

## Customisation

- Edit the `justfile` for your OS to add, remove, or change setup steps.
- Recipes are grouped by function (brew apps, CLI tools, productivity, etc.).
- You can run any step independently.

---

## Requirements

- Internet connection for downloads
- macOS: Xcode Command Line Tools (installed automatically)
- Linux: Build tools (build-essential), Python, etc. (installed automatically)
- Windows: PowerShell v3+, .NET 4.8+ (Chocolatey will prompt if missing)

---

## Environments \& Permissions

| Environment | Bootstrap Script | Justfile | Permissions | Notes |
| :-- | :-- | :-- | :-- | :-- |
| macOS | `sh/bootstrap_macos.sh` | `justfile` | sudo | Installs Homebrew, Xcode, just |
| Linux | `sh/bootstrap_linux.sh` | `just/justfile.linux` | sudo | Installs Homebrew (manual), just |
| Windows | `sh/bootstrap_windows.ps1` | `just/justfile.windows` | Administrator | Installs Chocolatey, just |
| Docker | See `Dockerfile` | `just/justfile.linux` | N/A (container) | Manual Homebrew install for reliability |
| Azure VM | As above | As above | Admin/sudo | Use in custom script or pipeline steps |



## Why use this?

- **Repeatable**: One command to set up a new machine or rebuild your environment.
- **Modular**: Tweak or extend recipes for your stack.
- **Cross-platform**: Consistent experience on Mac, Linux, and Windows.
- **Documented**: Your setup is version-controlled and easy to share.

---

## Future Plans

- Improve Linux and Windows support: Recipes and Dockerfile for robust Homebrew/just installation on Linux, and Chocolatey/just on Windows.
- Add CI/CD for automated setup testing
- Optional integration with dotfiles and secrets management

**Contributions and suggestions welcome via PR!**

---

## Appendix: Azure Infrastructure Context

**VMs**:
- Use bootstrap scripts as part of Azure VM Custom Script Extensions or during VM provisioning.

**DevOps Pipelines**:
- Integrate `justfile` recipes in Azure DevOps pipeline steps to ensure agents have the correct tools and directory structure.

**Cloud Shell**:
- For Linux-based agents, run the Linux bootstrap script; for Windows agents, run the PowerShell script.

**Permissions**:
- Ensure VMs or agents have administrator/sudo rights for package installation.

---

## Appendix: Xcode Command Line Tools (macOS only)

**What are they?**  
Xcode Command Line Tools are a set of essential developer utilities for macOS, including compilers (`clang`), build tools (`make`), version control (`git`), and other Unix utilities. These tools let you compile code, manage packages, and perform many programming tasks directly from the Terminal—without needing the full Xcode IDE.

**Why are they needed?**  
Out of the box, macOS does not include all the development tools required for programming. Many open source tools and package managers (like `Homebrew`) depend on these command-line utilities to function. Installing Xcode Command Line Tools ensures your system has the basic Unix-like environment expected by most development workflows. For example, `Homebrew` will prompt to install them if they are missing.

**How do you install them?**  
You can install Xcode Command Line Tools in several ways:
- **Via Terminal:**  
  Run `xcode-select --install` and follow the prompts.
- **Via Homebrew:**  
  Homebrew will automatically install them if needed during its setup.
- **Full Xcode:**  
  Installing the full Xcode IDE from the App Store also provides these tools, but this is unnecessary unless you are developing Apple platform apps.

**How does this compare to Linux/Windows?**  
- On **Linux**, developer tools (`gcc`, `make`, etc.) are usually installed via the system’s package manager (e.g., `apt`, `yum`, `dnf`), and are often pre-installed on developer-focused distributions.
- On **Windows**, development tools are provided via packages like MinGW, Visual Studio Build Tools, or Windows Subsystem for Linux (WSL), but are not included by default.

**In summary:**  
On macOS, installing Xcode Command Line Tools is the standard way to get a Unix-like development environment, similar to what Linux provides out of the box, and is a prerequisite for most programming, scripting, and automation tasks on macOS.
