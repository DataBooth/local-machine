from pathlib import Path
from zipfile import ZipFile
from loguru import logger
from plumbum import local, ProcessExecutionError
import os
from typing import List, Dict, Any


class CommandRunner:
    @staticmethod
    def run(command: str, *args, capture_output=True) -> str:
        logger.info(f"Running command: {command} {' '.join(args)}")
        try:
            cmd = local[command][args]
            result = cmd() if capture_output else cmd & local["cat"]
            logger.success(f"Command succeeded: {command} {' '.join(args)}")
            return result
        except ProcessExecutionError as e:
            # Special handling for crontab -l
            if command == "crontab" and "-l" in args and "no crontab for" in e.stderr:
                logger.warning("No user crontab found; treating as empty.")
                return ""
            logger.error(f"Command failed: {command} {' '.join(args)}\n{e.stderr}")
            return f"ERROR: {e.stderr}"


class DotfilesBackup:
    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir

    def backup(self) -> Path:
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        backup_file = self.backup_dir / f"dotfiles_backup_{self.timestamp()}.zip"
        dotfiles = [
            f for f in Path.home().glob(".*") if f.is_file() and f.name != ".DS_Store"
        ]
        logger.info(f"Backing up dotfiles: {[str(f) for f in dotfiles]}")
        with ZipFile(backup_file, "w") as zipf:
            for file in dotfiles:
                zipf.write(file, arcname=file.name)
        logger.success(f"Dotfiles backup created at {backup_file}")
        return backup_file

    @staticmethod
    def timestamp():
        from datetime import datetime

        return datetime.now().strftime("%Y%m%d_%H%M%S")


class BrewBackup:
    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir

    def backup(self) -> Path:
        brewfile = self.backup_dir / "Brewfile"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Dumping Brewfile...")
        CommandRunner.run("brew", "bundle", "dump", "--file", str(brewfile), "--force")
        logger.success(f"Brewfile created at {brewfile}")
        return brewfile

    def list_formulae(self) -> str:
        return CommandRunner.run("brew", "list", "--versions", "--formula")

    def list_casks(self) -> str:
        return CommandRunner.run("brew", "list", "--versions", "--cask")


class SSHKeysLister:
    def list_keys(self) -> List[str]:
        ssh_dir = Path.home() / ".ssh"
        keys = [
            f.name
            for f in ssh_dir.glob("*")
            if f.is_file() and not f.name.endswith(".pub")
        ]
        logger.info(f"SSH keys found: {keys}")
        return keys

    def show_config(self) -> str:
        config_file = Path.home() / ".ssh" / "config"
        if config_file.exists():
            content = config_file.read_text()
            logger.info("Loaded SSH config")
            return content
        logger.warning("No SSH config found")
        return "No SSH config found."


class MacOSInfo:
    def get_info(self) -> Dict[str, Any]:
        info = {}
        info["date"] = CommandRunner.run("date")
        info["macos_version"] = CommandRunner.run("sw_vers")
        info["applications"] = os.listdir("/Applications")
        logger.info("macOS info collected")
        return info


class VSCodeExtensions:
    def list_extensions(self) -> List[str]:
        output = CommandRunner.run("code", "--list-extensions", "--show-versions")
        extensions = output.strip().split("\n")
        logger.info(f"VS Code extensions found: {extensions}")
        return extensions

    def user_settings(self) -> str:
        settings_path = (
            Path.home() / "Library/Application Support/Code/User/settings.json"
        )
        if settings_path.exists():
            content = settings_path.read_text()
            logger.info("Loaded VS Code user settings")
            return content
        logger.warning("No VS Code user settings found")
        return "No VS Code user settings found."


class CrontabBackup:
    def export_crontab(self) -> str:
        output = CommandRunner.run("crontab", "-l")
        if output.strip() == "":
            logger.info("No user crontab found (empty output).")
            return "(No user crontab found)"
        logger.info("Exported user crontab")
        return output


class LaunchAgentsBackup:
    def list_agents(self) -> List[str]:
        agents_dir = Path.home() / "Library/LaunchAgents"
        if agents_dir.exists():
            agents = [f.name for f in agents_dir.glob("*.plist")]
            logger.info(f"LaunchAgents found: {agents}")
            return agents
        logger.warning("No LaunchAgents directory found")
        return []


class PipxList:
    def list_tools(self) -> str:
        output = CommandRunner.run("pipx", "list")
        logger.info("pipx list output captured")
        return output


class UVToolList:
    def list_tools(self) -> str:
        output = CommandRunner.run("uv", "tool", "list")
        logger.info("uv tool list output captured")
        return output
