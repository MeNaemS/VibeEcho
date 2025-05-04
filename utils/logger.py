from os.path import isdir
from os import makedirs
import logging


async def setup_logger(level: str = "INFO") -> None:
    if not isdir("logs"):
        makedirs("logs")
    logging.basicConfig(
        filename="logs/logs.log",
        format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        level=level,
        datefmt="%d.%m.%Y %H:%M:%S"
    )


async def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)
