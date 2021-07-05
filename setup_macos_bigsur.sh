# Capture the setup from my 12" MacBook (early 2015) - clean Big Sur install (11.4)

# move Dock to left

defaults write com.apple.dock orientation left
killall Dock

# Install Xcode tools (takes a few minutes)

xcode-select --install

# Install Homebrew - see https://brew.sh

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Get iTerm2 (replacement Terminal app)

brew install --cask iterm2
defaults write com.googlecode.iterm2 PromptOnQuit -bool false
