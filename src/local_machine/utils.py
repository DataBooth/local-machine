import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

from loguru import logger
from plumbum import ProcessExecutionError, local


class DotfilesBackup:
    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir

    def timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")


class DotfilesBackup:
    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir

    def timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def backup(self):
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = self.backup_dir / f"dotfiles_backup_{self.timestamp()}.zip"
        dotfiles = [
            f for f in Path.home().glob(".*") if f.is_file() and f.name != ".DS_Store"
        ]
        with zipfile.ZipFile(backup_file, "w") as zipf:
            for file in dotfiles:
                zipf.write(file, arcname=file.name)
        return backup_file


class BrewBackup:
    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir

    def backup(self):
        brewfile = self.backup_dir / "Brewfile"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        try:
            local["brew"]["bundle", "dump", "--file", str(brewfile), "--force"]()
            logger.info(f"Brewfile created at {brewfile}")
            return brewfile
        except ProcessExecutionError as e:
            logger.error(f"Brew bundle dump failed: {e.stderr}")
            return f"Error: {e.stderr}"

    def list_formulae(self):
        try:
            return local["brew"]["list", "--versions", "--formula"]()
        except ProcessExecutionError as e:
            logger.error(f"brew list --formula failed: {e.stderr}")
            return f"Error: {e.stderr}"

    def list_casks(self):
        try:
            return local["brew"]["list", "--versions", "--cask"]()
        except ProcessExecutionError as e:
            logger.error(f"brew list --cask failed: {e.stderr}")
            return f"Error: {e.stderr}"


class SSHKeysLister:
    def list_keys(self):
        ssh_dir = Path.home() / ".ssh"
        return [
            f.name
            for f in ssh_dir.glob("*")
            if f.is_file() and not f.name.endswith(".pub")
        ]

    def show_config(self):
        config_file = Path.home() / ".ssh" / "config"
        if config_file.exists():
            return config_file.read_text()
        return "No SSH config found."


class MacOSInfo:
    def get_info(self):
        info = {}
        try:
            info["date"] = local["date"]().strip()
        except ProcessExecutionError as e:
            info["date"] = f"Error: {e.stderr}"
        try:
            info["macos_version"] = local["sw_vers"]().strip()
        except ProcessExecutionError as e:
            info["macos_version"] = f"Error: {e.stderr}"
        try:
            info["applications"] = os.listdir("/Applications")
        except Exception as e:
            info["applications"] = f"Error: {e}"
        return info


class VSCodeExtensions:
    def list_extensions(self):
        try:
            output = local["code"]["--list-extensions", "--show-versions"]()
            return output.strip().splitlines()
        except ProcessExecutionError as e:
            logger.error(f"VS Code list-extensions failed: {e.stderr}")
            return [f"Error: {e.stderr}"]

    def user_settings(self):
        settings_path = (
            Path.home() / "Library/Application Support/Code/User/settings.json"
        )
        if settings_path.exists():
            return settings_path.read_text()
        return "No VS Code user settings found."


class CrontabBackup:
    def export_crontab(self):
        try:
            return local["crontab"]["-l"]()
        except ProcessExecutionError as e:
            logger.error(f"crontab -l failed: {e.stderr}")
            return f"Error: {e.stderr}"


class LaunchAgentsBackup:
    def list_agents(self):
        agents_dir = Path.home() / "Library/LaunchAgents"
        if agents_dir.exists():
            return [f.name for f in agents_dir.glob("*.plist")]
        return []


class PipxList:
    def list_tools(self):
        try:
            return local["pipx"]["list"]()
        except ProcessExecutionError as e:
            logger.error(f"pipx list failed: {e.stderr}")
            return f"Error: {e.stderr}"


class UVToolList:
    def list_tools(self):
        try:
            return local["uv"]["tool", "list"]()
        except ProcessExecutionError as e:
            logger.error(f"uv tool list failed: {e.stderr}")
            return f"Error: {e.stderr}"


class RBackup:
    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir

    def backup(self):
        files = [Path.home() / ".Rprofile", Path.home() / ".Renviron"]
        backed_up = []
        for f in files:
            if f.exists():
                dest = self.backup_dir / f.name
                shutil.copy(f, dest)
                backed_up.append(dest)
                logger.info(f"Copied {f} to {dest}")
        # RStudio config dirs
        rstudio_dirs = [
            Path.home() / ".config/rstudio",
            Path.home() / ".rstudio-desktop",
        ]
        for d in rstudio_dirs:
            if d.exists():
                archive = self.backup_dir / (d.name + "_backup")
                shutil.make_archive(str(archive), "zip", str(d))
                backed_up.append(str(archive) + ".zip")
                logger.info(f"Archived {d} to {archive}.zip")
        return backed_up if backed_up else ["No R or RStudio configs found."]


class GitBackup:
    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir

    def backup(self):
        files = [Path.home() / ".gitconfig", Path.home() / ".gitignore_global"]
        backed_up = []
        for f in files:
            if f.exists():
                dest = self.backup_dir / f.name
                shutil.copy(f, dest)
                backed_up.append(dest)
                logger.info(f"Copied {f} to {dest}")
        return backed_up if backed_up else ["No Git configs found."]


class TerminalBackup:
    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir

    def backup(self):
        backed_up = []
        # Warp config
        warp_dir = Path.home() / ".warp"
        if warp_dir.exists():
            archive = self.backup_dir / "warp_config"
            shutil.make_archive(str(archive), "zip", str(warp_dir))
            backed_up.append(str(archive) + ".zip")
            logger.info(f"Archived {warp_dir} to {archive}.zip")
        # Terminal.app and iTerm2 prefs
        prefs = [
            ("com.apple.Terminal.plist", "Terminal"),
            ("com.googlecode.iterm2.plist", "iTerm2"),
        ]
        for fname, label in prefs:
            src = Path.home() / "Library/Preferences" / fname
            if src.exists():
                dest = self.backup_dir / fname
                shutil.copy(src, dest)
                backed_up.append(dest)
                logger.info(f"Copied {label} prefs: {src} to {dest}")
        return backed_up if backed_up else ["No terminal configs found to backup."]


class CloudCLIsBackup:
    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir

    def backup(self):
        dirs = [
            (Path.home() / ".aws", "aws_config"),
            (Path.home() / ".config/gcloud", "gcloud_config"),
            (Path.home() / ".azure", "azure_config"),
            (Path.home() / ".railway", "railway_config"),
            (Path.home() / ".config/render", "render_config"),
        ]
        backed_up = []
        for src, name in dirs:
            if src.exists():
                archive = self.backup_dir / name
                shutil.make_archive(str(archive), "zip", str(src))
                backed_up.append(str(archive) + ".zip")
                logger.info(f"Archived {src} to {archive}.zip")
        return backed_up if backed_up else ["No Cloud CLI configs found."]


class DuckDBBackup:
    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir

    def backup(self):
        db = Path.home() / "duckdb.db"
        if db.exists():
            dest = self.backup_dir / db.name
            shutil.copy(db, dest)
            logger.info(f"Copied DuckDB database: {db} to {dest}")
            return [dest]
        else:
            logger.info("No DuckDB database found.")
            return ["No DuckDB database found."]


class SecretsBackup:
    def __init__(
        self, search_dir: Path = Path.home() / "code/github", venv_dir: str = ".venv"
    ):
        self.search_dir = search_dir
        self.venv_dir = venv_dir

    def report_table(self, patterns={".env", ".secrets.toml"}, progress_callback=None):
        secrets = []
        patterns = patterns
        all_dirs = [
            root
            for root, _, _ in os.walk(self.search_dir)
            if self.venv_dir not in Path(root).parts
        ]
        total = len(all_dirs)
        if total == 0:
            return secrets
        for i, root in enumerate(all_dirs):
            if progress_callback:
                progress_callback(i / total)
            for file in os.listdir(root):
                if file in patterns:
                    file_path = Path(root) / file
                    try:
                        stat = file_path.stat()
                        secrets.append(
                            {
                                "path": str(file_path),
                                "size_bytes": stat.st_size,
                                "last_modified": datetime.fromtimestamp(
                                    stat.st_mtime
                                ).isoformat(),
                            }
                        )
                    except Exception as e:
                        logger.error(f"Error accessing {file_path}: {e}")
        if progress_callback:
            progress_callback(1.0)
        return secrets
