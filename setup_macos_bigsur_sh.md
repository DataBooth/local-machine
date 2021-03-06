# Capture the setup from my 12" MacBook (early 2015) - clean Big Sur install (11.4)

# c.f. https://github.com/herrbischoff/awesome-macos-command-line  - lots of info here

# Display(s)

## Mirror displays - Press [command]+[F1] to toggle mirroring

# Dock

## move Dock to left

defaults write com.apple.dock orientation left && \
killall Dock

## Auto Rearrange Spaces Based on Most Recent Use

defaults write com.apple.dock mru-spaces -bool true && \
killall Dock

# Xcode command line tools

## Install Xcode tools (takes a few minutes)

xcode-select --install

# Homebrew (package management for macOS)

## Install Homebrew - see https://brew.sh

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Terminal 

## Get iTerm2 (replacement Terminal app)

brew install --cask iterm2
defaults write com.googlecode.iterm2 PromptOnQuit -bool false

## Close Terminal and open iTerm2

open /Applications/iTerm.app/

# iCloud Drive

## Create symbolic link for the iCloud drive (optional) i.e. cd ~/icloud

ln -s ~/Library/Mobile*Documents/com~apple~CloudDocs/ icloud

# Google Chrome browser

brew install --cask google-chrome

# Github.com

## Create Github coding directory

mkdir ~/code
cd code
mkdir github
cd github
mkdir DataBooth
mkdir mjboothaus

git config --global --edit

## Setup SSH key for Github - see docs on Slite

## Get the repo for this script to track any changes

git clone https://github.com/DataBooth/local-machine.git

# Code editor - Visual Studio Code

## Install Visual Studio Code

brew install --cask visual-studio-code

# NB: Enabled syncing of VSC settings via Github

## Install conda/mamba

brew install --cask mambaforge
conda init "$(basename "${SHELL}")"

# Productivity / Workflow Tools

## Flow (Workflow)

brew install --cask flow

## Slite (Knowledge management)

brew install --cask slite
