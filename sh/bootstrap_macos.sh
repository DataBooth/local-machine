#!/usr/bin/env bash

# chmod +x bootstrap.sh
# ./bootstrap.sh

set -e

echo "==> Checking for Homebrew..."
if ! command -v brew &>/dev/null; then
    echo "Installing Homebrew (will install Xcode Command Line Tools if needed)..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Add Homebrew to shell profile (Apple Silicon)
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >>~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "Homebrew already installed."
fi

echo "==> Checking for just..."
if ! command -v just &>/dev/null; then
    echo "Installing just..."
    brew install just
else
    echo "just already installed."
fi

echo "==> Bootstrap complete!
- Checked for and installed Homebrew (with Xcode Command Line Tools if needed)
- Checked for and installed just (command runner for modular setup)
Use 'just -f justfile.setup' to run the modular setup recipe(s) defined in justfile.setup."
