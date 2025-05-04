from typing import List
from dataclasses import dataclass
from dynaconf import Dynaconf
from .adapter_config import global_retort


@dataclass(slots=True)
class Dialog:
    size: List[int]
    error_image_path: str
    warning_image_path: str
    info_image_path: str


@dataclass(slots=True)
class App:
    name: str
    size: List[int]
    icon_path: str
    dialog: Dialog


@dataclass(slots=True)
class AppConfig:
    debug: bool
    log_level: str
    app: App

    @staticmethod
    async def load() -> "AppConfig":
        return global_retort.load(
            Dynaconf(
                settings_files=["config.toml"],
                environments=True,
                default_env="default",
                merge_enabled=True,
                dotenv=True
            ),
            AppConfig
        )
