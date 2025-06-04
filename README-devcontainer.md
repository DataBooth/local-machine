# Dev Container & GitHub Codespaces

This project includes a **Dev Container configuration** (`.devcontainer`) for [GitHub Codespaces](https://github.com/features/codespaces) and local VS Code Dev Containers.  
It provides a reproducible, cloud-based development environment that closely mirrors the local and Dockerized setups used for data science and engineering.

---

## Features

- Automated setup of core tools (Python, just, CLI utilities)
- Runs your `justfile` recipes for directory and environment initialization
- Pre-installs recommended VS Code extensions
- Suitable for both Codespaces and local VS Code Dev Containers

---

## Quick Start

1. **Open in Codespaces:**
   - Click the **Code** button in GitHub, then the **Codespaces** tab, and create a new codespace.
   - The environment will be built automatically using the `.devcontainer` configuration.

2. **Or open locally in VS Code:**
   - Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
   - Open the repository in VS Code.
   - Press `F1` and select **Dev Containers: Reopen in Container**.

3. **Wait for setup:**
   - On first launch, the container will install all dependencies and run the `postCreateCommand`, which typically calls `just core` or your preferred setup recipe.

---

## Configuration Overview

- **`.devcontainer/devcontainer.json`**  
  Main configuration file specifying the base image, setup commands, and VS Code extensions.
- **`.devcontainer/Dockerfile`** (optional)  
  Customizes the environment further, e.g., for ARM64 or extra tools.
- **`justfile`**  
  Defines modular setup recipes (directories, tools, etc.) run automatically after build.

### Example `devcontainer.json`
```json
{
  "name": "Data Science/Engineering Dev Env",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/python:1": {},
    "ghcr.io/devcontainers/features/node:1": {}
  },
  "postCreateCommand": "curl -fsSL https://just.systems/install.sh | bash -s -- --to /usr/local/bin && just core",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-toolsai.jupyter",
        "eamodio.gitlens",
        "github.copilot"
      ]
    }
  },
  "forwardPorts": [8888, 8501],
  "remoteUser": "vscode"
}
```

---

## Customization

- **Update the `postCreateCommand`** to run your preferred justfile recipe (e.g., `just core`, `just all`, or a custom setup).
- **Add or remove VS Code extensions** in the `customizations.vscode.extensions` array.
- **Modify the Dockerfile** if you need additional system dependencies or want to match your local/Docker setup more closely.

---

## Advanced: Multiple Dev Container Templates

If you want to provide alternative setups (e.g., for Python, C++, or data science), you can add multiple `devcontainer.json` files in subdirectories of `.devcontainer`[2][3]:
```
.devcontainer/
  python/
    devcontainer.json
  cpp/
    devcontainer.json
```
Users can select their preferred environment when creating a codespace.

---

## References

- [Introduction to dev containers – GitHub Docs][2]
- [Creating a codespace from a template][6]
- [Dev Container Templates – GitHub][1]
- [Example Codespaces devcontainer.json][8]

---

**This setup ensures your Codespace matches your local and Dockerized environments, making onboarding and collaboration seamless and reproducible.**  

For more, see the `.devcontainer` directory and your `justfile`.
