# `local-machine`

Shell scripts and [justfile](https://github.com/casey/just) recipes for setting up and configuring Mac laptops for data science and engineering.

- [`local-machine`](#local-machine)
  - [Features](#features)
  - [Quick Start](#quick-start)
    - [1. Clone this repository](#1-clone-this-repository)
    - [2. Bootstrap your Mac (first time only)](#2-bootstrap-your-mac-first-time-only)
    - [3. Run setup recipes](#3-run-setup-recipes)
  - [Structure](#structure)
  - [Customisation](#customisation)
  - [Requirements](#requirements)
  - [Why use this?](#why-use-this)
  - [Future Plans](#future-plans)
  - [Credits](#credits)
  - [Appendix: Xcode Command Line Tools](#appendix-xcode-command-line-tools)


---

## Features

- **Automated MacBook setup** for data science/engineering
- Modular, repeatable setup using [`just`](https://just.systems/man/en/)
- Includes Homebrew, Xcode tools, productivity apps, CLI tools, and more
- Easily customisable for your own stack

---

## Quick Start

### 1. Clone this repository

```sh
git clone https://github.com/DataBooth/local-machine.git
cd local-machine
```

### 2. Bootstrap your Mac (first time only)

This script installs Xcode Command Line Tools, Homebrew, and `just` if they are not already present.

```sh
chmod +x bootstrap.sh
./bootstrap.sh
```

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

See the [`justfile`](./justfile) for all available recipes.

---

## Structure

- `bootstrap.sh` – Bootstraps your Mac with Xcode tools, Homebrew, and just.
- `justfile` – Modular, repeatable setup recipes (edit to suit your needs).
- Additional shell scripts or configuration files as needed.

---

## Customisation

- Edit the `justfile` to add, remove, or change setup steps.
- Recipes are grouped by function (brew apps, CLI tools, productivity, etc.).
- You can run any step independently.

---

## Requirements

- macOS (tested on Big Sur 11.4 and newer)
- Internet connection for downloads

---

## Why use this?

- **Repeatable**: One command to set up a new Mac or rebuild your environment.
- **Modular**: Tweak or extend recipes for your stack.
- **Documented**: Your setup is version-controlled and easy to share.

---

## Future Plans

- Add CI/CD for automated setup testing
- Recipes for Linux and Windows
- Optional integration with dotfiles and secrets management

---

## Credits

- Inspired by [awesome-macos-command-line](https://github.com/herrbischoff/awesome-macos-command-line)
- Uses [just](https://github.com/casey/just) for task automation

---

**Contributions and suggestions welcome!**


---

## Appendix: Xcode Command Line Tools

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
