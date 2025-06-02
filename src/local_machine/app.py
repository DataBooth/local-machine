from pathlib import Path

import streamlit as st
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


class MacBackupApp:
    def __init__(self, config):
        self.config = config
        self.backup_dir = Path(
            self.config.get("backup", "dir", default=str(Path.home() / "icloud/backup"))
        )

        self.dotfiles = DotfilesBackup(self.backup_dir)
        self.brew = BrewBackup(self.backup_dir)
        self.ssh = SSHKeysLister()
        self.macos = MacOSInfo()
        self.vscode = VSCodeExtensions()
        self.crontab = CrontabBackup()
        self.launchagents = LaunchAgentsBackup()
        self.pipx = PipxList()
        self.uvtool = UVToolList()

    def run(self):
        st.title("MacBook Configuration Backup")

        tabs = st.tabs(
            [
                "Dotfiles",
                "Homebrew",
                "SSH Keys",
                "macOS Info",
                "VS Code",
                "Crontab",
                "LaunchAgents",
                "pipx",
                "uv",
            ]
        )

        with tabs[0]:
            st.header("Dotfiles")
            if st.button("Backup Dotfiles"):
                backup_file = self.dotfiles.backup()
                st.success(f"Dotfiles backup created at {backup_file}")
            st.write(
                [
                    str(f)
                    for f in Path.home().glob(".*")
                    if f.is_file() and f.name != ".DS_Store"
                ]
            )

        with tabs[1]:
            st.header("Homebrew")
            if st.button("Backup Brewfile"):
                brewfile = self.brew.backup()
                st.success(f"Brewfile created at {brewfile}")
            st.subheader("Formulae")
            st.code(self.brew.list_formulae())
            st.subheader("Casks")
            st.code(self.brew.list_casks())

        with tabs[2]:
            st.header("SSH Keys")
            st.write(self.ssh.list_keys())
            st.subheader("SSH Config")
            st.code(self.ssh.show_config())

        with tabs[3]:
            st.header("macOS Info")
            info = self.macos.get_info()
            st.write({"Date": info["date"], "macOS Version": info["macos_version"]})
            st.subheader("Installed Applications")
            st.write(info["applications"])

        with tabs[4]:
            st.header("VS Code Extensions")
            st.write(self.vscode.list_extensions())
            st.subheader("User Settings")
            st.code(self.vscode.user_settings())

        with tabs[5]:
            st.header("Crontab")
            st.code(self.crontab.export_crontab())

        with tabs[6]:
            st.header("LaunchAgents")
            st.write(self.launchagents.list_agents())

        with tabs[7]:
            st.header("pipx Tools")
            st.code(self.pipx.list_tools())

        with tabs[8]:
            st.header("uv Tools")
            st.code(self.uvtool.list_tools())


if __name__ == "__main__":
    from local_machine.config import ProjectConfig

    logger.add("backup.log", rotation="1 week")
    config = ProjectConfig()
    app = MacBackupApp(config)
    app.run()
