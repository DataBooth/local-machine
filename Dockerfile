FROM ubuntu:24.04

# Install core dependencies and tools
RUN apt-get update && \
    apt-get install -y sudo locales nano build-essential git curl wget python3 python3-pip

# Set locale
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Create a non-root user for development
RUN useradd -ms /bin/bash devuser && echo "devuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER devuser
WORKDIR /home/devuser

# Manually install Homebrew (recommended for Docker)
RUN git clone https://github.com/Homebrew/brew ~/.linuxbrew/Homebrew && \
    mkdir -p ~/.linuxbrew/bin && \
    ln -s ../Homebrew/bin/brew ~/.linuxbrew/bin/brew && \
    eval "$(/home/devuser/.linuxbrew/bin/brew shellenv)" && \
    /home/devuser/.linuxbrew/bin/brew update --force --quiet

# Add Homebrew to PATH for all subsequent steps
ENV PATH="/home/devuser/.linuxbrew/bin:/home/devuser/.linuxbrew/sbin:${PATH}"

# Debug: Confirm brew is in PATH and works
RUN which brew && brew --version

# Install just using Homebrew
RUN brew install just

# Debug: Confirm just is in PATH and works
RUN which just && just --version

# Copy your setup scripts and justfile into the container
COPY --chown=devuser:devuser sh/bootstrap_linux.sh ./bootstrap_linux.sh
COPY --chown=devuser:devuser just/justfile.linux ./justfile

RUN chmod +x ./bootstrap_linux.sh

CMD ["/bin/bash"]
