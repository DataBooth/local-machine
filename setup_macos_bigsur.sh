# Capture the setup from my 12" MacBook (early 2015) - clean Big Sur install (11.4)

## iCloud **** make sure Photos are turned off **** use for Notes, KeyChain

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

### Notes: on new MacBook
* After completion of Homebrew install:
** `echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/mjboothaus/.zprofile`
** `eval "$(/opt/homebrew/bin/brew shellenv)"`

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

## Rosetta for running Intel apps on M1 (currently Flow and Slite are Intel apps)

/usr/sbin/softwareupdate --install-rosetta --agree-to-license

## DB Browser for SQLite

brew install --cask db-browser-for-sqlite

## LibreOffice

brew install --cask libreoffice

## Flow (Workflow)

brew install --cask flow

## Slite (Knowledge management)

brew install --cask slite

## Break reminders (Time Out)
brew install --cask time-out

## OneDrive sync (5GB free storage & can access Office Online)

brew install --cask onedrive

# Other Command Line Tools

## tree

brew install tree

## OpenBLAS - for install of numpy etc which is failing on M1

brew install openblas
# export LDFLAGS="-L/opt/homebrew/opt/openblas/lib"
# export CPPFLAGS="-I/opt/homebrew/opt/openblas/include"

## pipx

brew install pipx
pipx ensurepath

## poetry

brew install poetry

## just (like make)

brew install just

## Sphinx-doc

pipx install Sphinx

## Black (code linter)

brew install black

## Hugo - static website generator

brew install hugo

# Data

## Datasette.io

brew install datasette

# Docker

## Docker Desktop

brew install --cask docker

## Disk Drill (find files / disk usage)

brew install --cask disk-drill

## Spyder (Scientific Python IDE)

brew install --cask spyder

## SQLFluff

pipx install sqlfluff

## Node

brew install node

## ImageMagick

brew install imagemagick

## Rectangle - Window manager

brew install --cask rectangle

## wget

brew install wget

## yarn - Javascript package manager

brew install yarn

## PyScaffold

pipx install pyscaffold

## Pandoc - Document conversions

brew install pandoc

## CSV Kit

brew install csvkit

## Diff tool

brew install diffr

## PostgreSQL

brew install postgresql

brew install --cask pgadmin4

# marp.app

brew install marp-cli
