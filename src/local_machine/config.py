from pathlib import Path
from typing import Optional, List, Any, Dict, Union
import os
import tomllib
from loguru import logger
from dotenv import load_dotenv, find_dotenv


class ProjectConfig:
    """
    Loads and manages configuration from TOML files and environment variables.
    """

    def __init__(
        self,
        conf_dir: str = "conf",
        toml_files: Optional[List[Union[str, Path]]] = None,
        project_root_marker: str = "pyproject.toml",
        start_dir: Optional[Union[str, Path]] = None,
        dotenv_file: str = ".env",
    ) -> None:
        logger.info("Initialising ProjectConfig")
        self.project_root: Path = self.find_project_root(
            marker=project_root_marker, start_dir=start_dir
        )
        logger.info(f"Project root found: {self.project_root}")

        self.conf_dir: Path = (self.project_root / conf_dir).resolve()
        logger.info(f"Config directory set to: {self.conf_dir}")

        if toml_files is not None:
            self.toml_files: List[Path] = [self.conf_dir / Path(f) for f in toml_files]
        else:
            self.toml_files: List[Path] = sorted(self.conf_dir.glob("*.toml"))
        logger.info(f"TOML files to load: {[str(f) for f in self.toml_files]}")

        self.configs: Dict[str, dict] = self._load_all()
        self._load_dotenv(dotenv_file=dotenv_file)

    @staticmethod
    def find_project_root(
        marker: str = "pyproject.toml", start_dir: Optional[Union[str, Path]] = None
    ) -> Path:
        current = Path(start_dir).resolve() if start_dir else Path.cwd()
        logger.debug(f"Searching for project root from: {current}")
        while current != current.parent:
            logger.debug(f"Checking for {marker} in {current}")
            if (current / marker).exists():
                logger.success(f"Found project root at: {current}")
                return current
            current = current.parent
        logger.error(f"Could not find project root (missing {marker})")
        raise FileNotFoundError(f"Could not find project root (missing {marker})")

    def _load_all(self) -> Dict[str, dict]:
        configs: Dict[str, dict] = {}
        for f in self.toml_files:
            logger.info(f"Loading TOML config: {f}")
            with open(f, "rb") as fp:
                configs[f.stem] = tomllib.load(fp)
        logger.success("All TOML configs loaded successfully")
        return configs

    def _load_dotenv(self, dotenv_file: str) -> None:
        env_path = find_dotenv(str(self.project_root / dotenv_file))
        if env_path:
            logger.info(f"Loading environment variables from {env_path}")
            load_dotenv(env_path)
            logger.success("Environment variables loaded from .env")
        else:
            logger.warning(f"No .env file found at {self.project_root / dotenv_file}")

    def get(self, *keys: str, file: Optional[str] = None, default: Any = None) -> Any:
        logger.debug(
            f"Getting config value: keys={keys}, file={file}, default={default}"
        )
        sources = [file] if file else self.configs.keys()
        for src in sources:
            conf = self.configs.get(src, {})
            val = conf
            for k in keys:
                if isinstance(val, dict) and k in val:
                    val = val[k]
                else:
                    val = None
                    break
            if val is not None:
                logger.info(f"Found value for {keys} in {src}: {val}")
                return val
        logger.warning(f"Config value {keys} not found, returning default: {default}")
        return default

    @staticmethod
    def get_env(key: str, default: Any = None) -> Optional[str]:
        value = os.getenv(key, default)
        if value is not None:
            logger.info(f"Environment variable '{key}' found: {value}")
        else:
            logger.warning(
                f"Environment variable '{key}' not found, using default: {default}"
            )
        return value

    def as_dict(self) -> Dict[str, dict]:
        return dict(self.configs)

    def debug_print(self) -> None:
        import pprint

        pprint.pprint(self.as_dict())
