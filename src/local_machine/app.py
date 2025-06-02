from pathlib import Path
import streamlit as st
from loguru import logger
import pandas as pd
import plistlib

from local_machine.utils import (
    DotfilesBackup,
    BrewBackup,
    SSHKeysLister,
    MacOSInfo,
    VSCodeExtensions,
    CrontabBackup,
    LaunchAgentsBackup,
    PipxList,
    UVToolList,
    RBackup,
    GitBackup,
    TerminalBackup,
    CloudCLIsBackup,
    DuckDBBackup,
    SecretsBackup,
)


class MacBackupApp:
    def __init__(self, config, tabs_list=None):
        self.config = config
        self.tabs_list = tabs_list or [
            "Dotfiles",
            "Homebrew",
            "SSH Keys",
            "macOS Info",
            "VS Code",
            "Crontab",
            "LaunchAgents",
            "Python tools",
            "R",
            "Git",
            "Terminal",
            "Cloud CLIs",
            "DuckDB",
            "Secrets",
        ]
        self.backup_dir = Path(
            self.config.get("backup", "dir", default=str(Path.home() / "icloud/backup"))
        )

        # Initialize all backup utilities
        self.backup_utils = {
            "Dotfiles": DotfilesBackup(self.backup_dir),
            "Homebrew": BrewBackup(self.backup_dir),
            "SSH Keys": SSHKeysLister(),
            "macOS Info": MacOSInfo(),
            "VS Code": VSCodeExtensions(),
            "Crontab": CrontabBackup(),
            "LaunchAgents": LaunchAgentsBackup(),
            "Python tools": {"uv": UVToolList(), "pipx": PipxList()},
            "R": RBackup(self.backup_dir),
            "Git": GitBackup(self.backup_dir),
            "Terminal": TerminalBackup(self.backup_dir),
            "Cloud CLIs": CloudCLIsBackup(self.backup_dir),
            "DuckDB": DuckDBBackup(self.backup_dir),
            "Secrets": SecretsBackup(),
        }

    def run(self):
        st.set_page_config(
            page_title="MacBook Configuration Backup",
            page_icon=":floppy_disk:",
            layout="wide",
        )
        st.title("MacBook Configuration Backup")

        tabs = st.tabs(self.tabs_list)
        tab_indices = {name: idx for idx, name in enumerate(self.tabs_list)}

        # Dotfiles Tab
        if "Dotfiles" in tab_indices:
            with tabs[tab_indices["Dotfiles"]]:
                st.header("Dotfiles")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Show Dotfiles", key="dotfiles_show"):
                        files = [
                            str(f)
                            for f in Path.home().glob(".*")
                            if f.is_file() and f.name != ".DS_Store"
                        ]
                        st.write(files)
                with col2:
                    if st.button("Backup Dotfiles", key="dotfiles_backup"):
                        backup_file = self.backup_utils["Dotfiles"].backup()
                        st.success("Dotfiles backup complete!")
                        st.code(f"Backup file: {backup_file}")

        # Homebrew Tab
        if "Homebrew" in tab_indices:
            with tabs[tab_indices["Homebrew"]]:
                st.header("Homebrew")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Show Packages", key="homebrew_show"):
                        st.subheader("Formulae")
                        st.code(self.backup_utils["Homebrew"].list_formulae())
                        st.subheader("Casks")
                        st.code(self.backup_utils["Homebrew"].list_casks())
                with col2:
                    if st.button("Backup Brewfile", key="homebrew_backup"):
                        brewfile = self.backup_utils["Homebrew"].backup()
                        st.success("Brewfile backup complete!")
                        st.code(f"Backup file: {brewfile}")

        # SSH Keys Tab
        if "SSH Keys" in tab_indices:
            with tabs[tab_indices["SSH Keys"]]:
                st.header("SSH Keys")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Show SSH Keys", key="sshkeys_show"):
                        st.write(self.backup_utils["SSH Keys"].list_keys())
                with col2:
                    if st.button("Show SSH Config", key="sshkeys_config"):
                        st.code(self.backup_utils["SSH Keys"].show_config())

        # macOS Info Tab
        if "macOS Info" in tab_indices:
            with tabs[tab_indices["macOS Info"]]:
                st.header("macOS Info")
                if st.button("Show System Info", key="macosinfo_show"):
                    info = self.backup_utils["macOS Info"].get_info()
                    st.write(
                        {"Date": info["date"], "macOS Version": info["macos_version"]}
                    )
                    st.subheader("Installed Applications")
                    st.write(info["applications"])

        # VS Code Tab
        if "VS Code" in tab_indices:
            with tabs[tab_indices["VS Code"]]:
                st.header("VS Code")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Show Extensions", key="vscode_ext_show"):
                        st.write(self.backup_utils["VS Code"].list_extensions())
                with col2:
                    if st.button("Show Settings", key="vscode_settings_show"):
                        st.code(self.backup_utils["VS Code"].user_settings())

        # Crontab Tab
        if "Crontab" in tab_indices:
            with tabs[tab_indices["Crontab"]]:
                st.header("Crontab")
                if st.button("Show Crontab", key="crontab_show"):
                    st.code(self.backup_utils["Crontab"].export_crontab())

        # LaunchAgents Tab
        if "LaunchAgents" in tab_indices:
            with tabs[tab_indices["LaunchAgents"]]:
                st.header("LaunchAgents")
                if st.button("Show LaunchAgents", key="launchagents_show"):
                    st.write(self.backup_utils["LaunchAgents"].list_agents())

        # Python Tools Tab
        if "Python tools" in tab_indices:
            with tabs[tab_indices["Python tools"]]:
                st.header("Python Tools")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Show uv Tools", key="uvtools_show"):
                        st.code(self.backup_utils["Python tools"]["uv"].list_tools())
                with col2:
                    if st.button("Show pipx Tools", key="pipx_show"):
                        st.code(self.backup_utils["Python tools"]["pipx"].list_tools())

        # R Tab
        if "R" in tab_indices:
            with tabs[tab_indices["R"]]:
                st.header("R and RStudio")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Show Configs", key="r_show"):
                        rprofile = Path.home() / ".Rprofile"
                        renviron = Path.home() / ".Renviron"
                        if rprofile.exists():
                            st.subheader(".Rprofile")
                            st.code(rprofile.read_text())
                        if renviron.exists():
                            st.subheader(".Renviron")
                            st.code(renviron.read_text())
                with col2:
                    if st.button("Backup R Configs", key="r_backup"):
                        files = self.backup_utils["R"].backup()
                        st.success("R backup complete!")
                        for f in files:
                            st.code(f"Backup file: {f}")

        # Git Tab
        if "Git" in tab_indices:
            with tabs[tab_indices["Git"]]:
                st.header("Git Configs")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Show Configs", key="git_show"):
                        gitconfig = Path.home() / ".gitconfig"
                        gitignore = Path.home() / ".gitignore_global"
                        if gitconfig.exists():
                            st.subheader(".gitconfig")
                            st.code(gitconfig.read_text())
                        if gitignore.exists():
                            st.subheader(".gitignore_global")
                            st.code(gitignore.read_text())
                with col2:
                    if st.button("Backup Git Configs", key="git_backup"):
                        files = self.backup_utils["Git"].backup()
                        st.success("Git backup complete!")
                        for f in files:
                            st.code(f"Backup file: {f}")

        # Terminal Tab
        if "Terminal" in tab_indices:
            with tabs[tab_indices["Terminal"]]:
                st.header("Terminal Apps")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Show Configs", key="terminal_show"):
                        term_plist = (
                            Path.home() / "Library/Preferences/com.apple.Terminal.plist"
                        )
                        iterm_plist = (
                            Path.home()
                            / "Library/Preferences/com.googlecode.iterm2.plist"
                        )
                        for plist_file in [term_plist, iterm_plist]:
                            if plist_file.exists():
                                st.subheader(plist_file.name)
                                try:
                                    with open(plist_file, "rb") as f:
                                        content = plistlib.load(f)
                                    st.json(content)
                                except Exception:
                                    st.code(plist_file.read_text(errors="replace"))
                with col2:
                    if st.button("Backup Terminal Configs", key="terminal_backup"):
                        files = self.backup_utils["Terminal"].backup()
                        st.success("Terminal backup complete!")
                        for f in files:
                            st.code(f"Backup file: {f}")

        # Cloud CLIs Tab
        if "Cloud CLIs" in tab_indices:
            with tabs[tab_indices["Cloud CLIs"]]:
                st.header("Cloud CLI Tools")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Show Configs", key="cloudcli_show"):
                        for label, path in [
                            ("AWS", Path.home() / ".aws"),
                            ("GCloud", Path.home() / ".config/gcloud"),
                            ("Azure", Path.home() / ".azure"),
                        ]:
                            if path.exists():
                                st.subheader(f"{label} Config")
                                st.write(list(path.glob("**/*")))
                with col2:
                    if st.button("Backup Cloud Configs", key="cloudcli_backup"):
                        files = self.backup_utils["Cloud CLIs"].backup()
                        st.success("Cloud backup complete!")
                        for f in files:
                            st.code(f"Backup file: {f}")

        # DuckDB Tab
        if "DuckDB" in tab_indices:
            with tabs[tab_indices["DuckDB"]]:
                st.header("DuckDB")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Show Database Info", key="duckdb_show"):
                        db = Path.home() / "duckdb.db"
                        if db.exists():
                            st.write(f"Database location: {db}")
                            st.write(f"Size: {db.stat().st_size / 1024:.1f} KB")
                with col2:
                    if st.button("Backup DuckDB", key="duckdb_backup"):
                        files = self.backup_utils["DuckDB"].backup()
                        st.success("DuckDB backup complete!")
                        for f in files:
                            st.code(f"Backup file: {f}")

        # Secrets Tab
        if "Secrets" in tab_indices:
            with tabs[tab_indices["Secrets"]]:
                st.header("Secrets Audit")
                if st.button("Scan for Secrets", key="secrets_show"):
                    with st.spinner("Scanning for secret files..."):
                        progress = st.progress(0)
                        secrets = self.backup_utils["Secrets"].report_table(
                            progress_callback=progress.progress
                        )
                    if not secrets:
                        st.info("No .env or .secrets.toml files found")
                    else:
                        st.write("Secret files found:")
                        st.dataframe(pd.DataFrame(secrets))


if __name__ == "__main__":
    from local_machine.config import ProjectConfig

    logger.add("backup.log", rotation="1 week")
    config = ProjectConfig()

    # Get tabs list from config, with fallback
    tabs_list = config.get(
        "ui",
        "tabs",
        default=[
            "Dotfiles",
            "Homebrew",
            "SSH Keys",
            "macOS Info",
            "VS Code",
            "Crontab",
            "LaunchAgents",
            "Python tools",
            "R",
            "Git",
            "Terminal",
            "Cloud CLIs",
            "DuckDB",
            "Secrets",
        ],
    )

    app = MacBackupApp(config, tabs_list=tabs_list)
    app.run()
