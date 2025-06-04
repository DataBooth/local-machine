# README_justfile-setup.md

## Overview

This repository uses **justfiles** to define modular, cross-platform developer environment setup recipes. Justfiles automate directory creation, documentation, and tool installation, ensuring consistent environments across macOS, Linux, and Windows.

## Approach

- **Parameterisation:**  
  User-specific and company-specific values are passed as variables, making recipes reusable and shareable.
- **Directory Setup:**  
  Recipes create standardised code and data directories with README files.
- **Tool Installation:**  
  Recipes invoke package managers (`brew`, `apt`, `choco`) to install core and optional tools.
- **Cross-platform:**  
  Separate justfiles for Linux (`justfile.linux`), macOS (`justfile.macos`), and Windows (`justfile.windows`).

## Environments & Requirements

| OS         | justfile              | Package Manager | Shell         | Just Installation Method          | Permissions Needed      |
|------------|-----------------------|-----------------|---------------|-----------------------------------|------------------------|
| Linux      | `justfile.linux`      | apt/brew        | Bash          | Homebrew or apt                   | sudo (for apt/brew)    |
| macOS      | `justfile.macos`      | brew            | Bash/zsh      | Homebrew                          | sudo (for brew)        |
| Windows    | `justfile.windows`    | choco           | PowerShell/cmd| Chocolatey (`choco install just`) | Admin (for choco)      |

## Usage

### General

- **Set variables at runtime or in the justfile:**
  ```sh
  just github-dirs personal_name=alice company_name=acme
  ```
- **Run core setup:**
  ```sh
  just core personal_name=alice company_name=acme
  ```

### Windows

- Ensure `just` is installed (`choco install just`).
- Run recipes from PowerShell or cmd.

### Linux/macOS

- Ensure `just` is installed (`brew install just` or `apt install just`).
- Run recipes from Bash or zsh.

## Azure Infrastructure Context

- **VM Customisation:**  
  Use justfiles as part of Azure VM provisioning scripts to standardise dev environments for teams.
- **DevOps Agents:**  
  Run justfile recipes in Azure DevOps pipeline steps to ensure agents have the correct tools and directory structure.
- **Permissions:**  
  Agents or VMs must have admin/sudo rights for initial package installation.

---

## **Summary Table**

| Environment      | Bootstrap Script         | Justfile           | Permissions         | Notes                                   |
|------------------|-------------------------|--------------------|---------------------|-----------------------------------------|
| Windows          | PowerShell (.ps1)       | justfile.windows   | Admin (for choco)   | Uses Chocolatey, PowerShell, Just       |
| macOS            | Bash (.sh)              | justfile.macos     | sudo (for brew)     | Uses Homebrew, Bash, Just               |
| Linux            | Bash (.sh)              | justfile.linux     | sudo (for apt/brew) | Uses apt, Homebrew, Bash, Just          |
| Azure VM/Agent   | As above                | As above           | Admin/sudo          | Use in custom script or pipeline steps  |

---

**This approach ensures reliable, repeatable, and cross-platform developer setups, suitable for both local machines and cloud infrastructure like Azure.**  

For more, see [Chocolatey requirements][1][2][3][5][6][7], [Azure VM custom script extension docs], and [Homebrew installation docs].

## References

[1] https://chocolatey.org/install  
[2] https://docs.chocolatey.org/en-us/choco/setup/  
[3] https://www.liquidweb.com/blog/how-to-install-chocolatey-on-windows/  
[4] https://docs.chocolatey.org/en-us/getting-started/  
[5] https://github.com/Vets-Who-Code/windows-dev-guide  
[6] https://github.com/berkanuslu/choco-development-enviroment-setup  
[7] https://www.xda-developers.com/simplify-pc-set-up-with-chocolatey-package-manager/  
[8] https://octopus.com/blog/chocolatey-powershell-and-runbooks  
[9] https://www.youtube.com/watch?v=BL6T15yEB_Q