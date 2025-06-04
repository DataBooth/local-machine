FROM ubuntu:24.04

RUN apt-get update && apt-get install -y sudo locales nano build-essential git curl wget python3 python3-pip

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Create a non-root user
RUN useradd -ms /bin/bash devuser && echo "devuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER devuser
WORKDIR /home/devuser

# Set environment variables for non-interactive Homebrew install
ENV NONINTERACTIVE=1

# Install Homebrew as devuser
RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH for all future RUN, CMD, and ENTRYPOINT instructions
ENV PATH="/home/devuser/.linuxbrew/bin:/home/devuser/.linuxbrew/sbin:${PATH}"

# Install just with Homebrew
RUN brew install just

# Copy your scripts and justfile
COPY --chown=devuser:devuser sh/bootstrap_linux.sh ./bootstrap_linux.sh
COPY --chown=devuser:devuser just/justfile.linux ./justfile

RUN chmod +x ./bootstrap_linux.sh

CMD ["/bin/bash"]
