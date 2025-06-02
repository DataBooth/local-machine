import argparse
from pathlib import Path

from loguru import logger

from local_machine.utils import (
    BrewBackup,
    CrontabBackup,
    DotfilesBackup,
    LaunchAgentsBackup,
    MacOSInfo,
    PipxList,
    SSHKeysLister,
    UVToolList,
    VSCodeExtensions,
)


def run_cli(args):
    backup_dir = args.backup_dir

    dotfiles = DotfilesBackup(backup_dir)
    brew = BrewBackup(backup_dir)
    ssh = SSHKeysLister()
    macos = MacOSInfo()
    vscode = VSCodeExtensions()
    crontab = CrontabBackup()
    launchagents = LaunchAgentsBackup()
    pipx = PipxList()
    uvtool = UVToolList()

    if args.action == "dotfiles" or args.action == "all":
        backup_file = dotfiles.backup()
        print(f"Dotfiles backup created at {backup_file}")

    if args.action == "brew" or args.action == "all":
        brewfile = brew.backup()
        print(f"Brewfile created at {brewfile}")
        print("Formulae:\n", brew.list_formulae())
        print("Casks:\n", brew.list_casks())

    if args.action == "ssh" or args.action == "all":
        print("SSH Keys:", ssh.list_keys())
        print("SSH Config:\n", ssh.show_config())

    if args.action == "macos" or args.action == "all":
        info = macos.get_info()
        print("Date:", info["date"])
        print("macOS Version:", info["macos_version"])
        print("Installed Applications:", info["applications"])

    if args.action == "vscode" or args.action == "all":
        print("VS Code Extensions:", vscode.list_extensions())
        print("VS Code User Settings:\n", vscode.user_settings())

    if args.action == "crontab" or args.action == "all":
        print("User Crontab:\n", crontab.export_crontab())

    if args.action == "launchagents" or args.action == "all":
        print("LaunchAgents:", launchagents.list_agents())

    if args.action == "pipx" or args.action == "all":
        print("pipx tools:\n", pipx.list_tools())

    if args.action == "uv" or args.action == "all":
        print("uv tools:\n", uvtool.list_tools())


def main():
    parser = argparse.ArgumentParser(description="MacBook Configuration Backup Utility")
    parser.add_argument("--ui", action="store_true", help="Run the Streamlit GUI app")
    parser.add_argument(
        "--backup-dir", type=Path, default=Path.home() / "icloud/backup"
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=[
            "dotfiles",
            "brew",
            "ssh",
            "macos",
            "vscode",
            "crontab",
            "launchagents",
            "pipx",
            "uv",
            "all",
        ],
        default="all",
    )
    args = parser.parse_args()

    logger.add("backup_main.log", rotation="1 week")

    if args.ui:
        # Only launch Streamlit if run as 'streamlit run main.py -- --ui'
        import streamlit as st
        from local_machine.config import (
            ProjectConfig,
        )
        from local_machine.app import MacBackupApp

        config = ProjectConfig()
        app = MacBackupApp(config)
        app.run()
    else:
        run_cli(args)


if __name__ == "__main__":
    main()
