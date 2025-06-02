import argparse
from pathlib import Path
from loguru import logger

from plumbum import local, FG

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


def run_cli(args):
    backup_dir = args.backup_dir
    dry_run = args.dry_run

    def maybe_write(fn, *a, **kw):
        if dry_run:
            print(f"[DRY RUN] Would run: {fn.__qualname__}")
            return "Dry run: no files written."
        return fn(*a, **kw)

    if args.action in ("dotfiles", "all"):
        result = maybe_write(DotfilesBackup(backup_dir).backup)
        print("Dotfiles backup:", result)

    if args.action in ("brew", "all"):
        result = maybe_write(BrewBackup(backup_dir).backup)
        print("Brewfile backup:", result)
        print("Formulae:\n", BrewBackup(backup_dir).list_formulae())
        print("Casks:\n", BrewBackup(backup_dir).list_casks())

    if args.action in ("ssh", "all"):
        print("SSH Keys:", SSHKeysLister().list_keys())
        print("SSH Config:\n", SSHKeysLister().show_config())

    if args.action in ("macos", "all"):
        info = MacOSInfo().get_info()
        print("Date:", info["date"])
        print("macOS Version:", info["macos_version"])
        print("Installed Applications:", info["applications"])

    if args.action in ("vscode", "all"):
        print("VS Code Extensions:", VSCodeExtensions().list_extensions())
        print("VS Code User Settings:\n", VSCodeExtensions().user_settings())

    if args.action in ("crontab", "all"):
        print("User Crontab:\n", CrontabBackup().export_crontab())

    if args.action in ("launchagents", "all"):
        print("LaunchAgents:", LaunchAgentsBackup().list_agents())

    if args.action in ("pipx", "all"):
        print("pipx tools:\n", PipxList().list_tools())

    if args.action in ("uv", "all"):
        print("uv tools:\n", UVToolList().list_tools())

    if args.action in ("r", "all"):
        result = maybe_write(RBackup(backup_dir).backup)
        print("R backup:", result)

    if args.action in ("git", "all"):
        result = maybe_write(GitBackup(backup_dir).backup)
        print("Git backup:", result)

    if args.action in ("terminal", "all"):
        result = maybe_write(TerminalBackup(backup_dir).backup)
        print("Terminal backup:", result)

    if args.action in ("cloud", "all"):
        result = maybe_write(CloudCLIsBackup(backup_dir).backup)
        print("Cloud CLI backup:", result)

    if args.action in ("duckdb", "all"):
        result = maybe_write(DuckDBBackup(backup_dir).backup)
        print("DuckDB backup:", result)

    if args.action in ("secrets", "all"):
        secrets = SecretsBackup().report_table()
        if not secrets:
            print("No .env or .secrets.toml files found.")
        else:
            print("Secrets found:")
            for entry in secrets:
                print(
                    f"{entry['path']} | {entry['size_bytes']} bytes | modified {entry['last_modified']}"
                )


def main():
    parser = argparse.ArgumentParser(description="MacBook Configuration Backup Utility")
    parser.add_argument("--ui", action="store_true", help="Run the Streamlit GUI app")
    parser.add_argument(
        "--backup-dir", type=Path, default=Path.home() / "icloud/backup"
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not write any files")
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
            "r",
            "git",
            "terminal",
            "cloud",
            "duckdb",
            "secrets",
            "all",
        ],
        default="all",
    )
    args = parser.parse_args()

    logger.add("backup_main.log", rotation="1 week")

    if args.ui:
        app_path = Path(__file__).parent.parent / "src" / "local_machine" / "app.py"
        if not app_path.exists():
            raise FileNotFoundError(f"Streamlit app not found at {app_path}")
        streamlit = local["streamlit"]
        streamlit["run", str(app_path)] & FG
    else:
        run_cli(args)


if __name__ == "__main__":
    main()
