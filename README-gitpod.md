# Gitpod Dev Container Setup

This repository supports [Gitpod](https://www.gitpod.io/) for one-click, cloud-based development environments that closely mirror your local and Codespaces setups.

---

## Features

- **Automated environment setup** using Dev Containers and [justfile](https://just.systems/) recipes
- **Consistent tooling**: Python, just, CLI utilities, VS Code extensions, and more
- **Runs your setup scripts and just recipes** on workspace start
- **Supports both single- and multi-container setups** (Docker Compose)
- **Easy onboarding**: new contributors can start coding immediately

---

## Quick Start

1. **Open in Gitpod**  
   Click the **Gitpod** button in your repo (or prefix your repo URL with `https://gitpod.io/#`).

2. **Wait for the environment to build**  
   Gitpod will use the `.devcontainer/devcontainer.json` (or `.devcontainer.json`) in your repo to provision the environment.

3. **Automated setup**  
   - On first start, Gitpod will run the `postCreateCommand` (from your devcontainer) or any tasks defined in `.gitpod/automations.yaml` to install tools and run your `just` recipes (e.g., `just core`).
   - Recommended VS Code extensions will be installed automatically.

---

## Configuration Overview

- **`.devcontainer/devcontainer.json`**  
  Defines the base image, tools, VS Code extensions, and post-creation commands.
- **`.gitpod/automations.yaml`** (optional)  
  Automates additional setup tasks (see below).
- **`justfile`**  
  Modular recipes for directory creation, tool installation, and environment configuration.

### Example `.devcontainer/devcontainer.json`
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

### Example `.gitpod/automations.yaml`
```yaml
tasks:
  setup:
    name: Setup environment
    command: just core
    triggeredBy:
      - postDevcontainerStart
      - manual
```
- Use automations to trigger your `just` recipes after the dev container starts or on demand[1][6].

---

## Customization

- **Edit your `justfile`** to add or adjust setup steps for tools, directories, or data.
- **Update `postCreateCommand`** or automations to run your preferred setup recipe.
- **Add/remove VS Code extensions** in `devcontainer.json` as needed.
- For multi-service projects, use Docker Compose and specify it in your `devcontainer.json` (`dockerComposeFile`, `service`, etc.)[1][2].

---

## Rebuilding & Iterating

- After changing your devcontainer or automation config, **rebuild the workspace**:
  - In VS Code, use the **Gitpod Flex: Rebuild Container** command.
  - Or run `gitpod environment devcontainer rebuild` from the terminal[1][4].

---

## References

- [Gitpod: Dev Container Configuration][2]
- [Gitpod: Automations][1][6]
- [Gitpod: Configure a dev environment][4]
- [Gitpod Docs: Dev Containers][2][6]
- [Dev Containers Spec][5]

---

**This setup ensures your Gitpod workspace matches your local and Codespaces environments, providing a fast, reproducible, and consistent developer experience.**  

For more, see the `.devcontainer` directory, `.gitpod/automations.yaml`, and your `justfile`.

---

[1]: https://www.gitpod.io/docs/gitpod/configuration/devcontainer/getting-started  
[2]: https://www.gitpod.io/docs/gitpod/configuration/devcontainer/overview  
[4]: https://www.gitpod.io/docs/gitpod/getting-started/configure-dev-environment  
[5]: https://cadu.dev/using-devcontainers-to-setup-your-dev-environment/  
[6]: https://www.gitpod.io/docs/gitpod/introduction/devcontainer

[1] https://www.gitpod.io/docs/gitpod/configuration/devcontainer/getting-started
[2] https://www.gitpod.io/docs/gitpod/configuration/devcontainer/overview
[3] https://www.youtube.com/watch?v=C-aV16phypg
[4] https://www.gitpod.io/docs/gitpod/getting-started/configure-dev-environment
[5] https://cadu.dev/using-devcontainers-to-setup-your-dev-environment/
[6] https://www.gitpod.io/docs/gitpod/introduction/devcontainer
[7] https://www.gitpod.io/docs/gitpod/introduction/overview
[8] https://www.youtube.com/watch?v=71pmCfLdxTg