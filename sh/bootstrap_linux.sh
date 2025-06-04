#!/usr/bin/env bash
set -e

echo "==> Updating package lists..."
sudo apt-get update

echo "==> Installing core packages..."
sudo apt-get install -y build-essential git curl wget python3 python3-pip

echo "==> Checking for Homebrew/Linuxbrew..."
if ! command -v brew &>/dev/null; then
    echo "Installing Homebrew/Linuxbrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >>~/.profile
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
else
    echo "Homebrew already installed."
fi

echo "==> Installing just..."
brew install just

echo "==> Bootstrap complete!
- Installed essential build tools and Python
- Installed Homebrew/Linuxbrew
- Installed just task runner
You can now use 'just' to run modular setup recipes defined in your justfile."
