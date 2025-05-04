from typing import Tuple
from dishka import make_async_container, AsyncContainer
from PySide6.QtWidgets import QApplication
from qdarkstyle import load_stylesheet_pyside6
from qasync import QEventLoop
from sys import argv, exit
from adaptix import Retort
from logging import Logger
from services.song import SongService
import asyncio
from container import AppProvider
from ui.main_window import MainWindow
from config.config import AppConfig


def main() -> None:
    app: QApplication = QApplication(argv)
    app.setStyleSheet(load_stylesheet_pyside6())
    loop: QEventLoop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    async def run() -> Tuple[AppConfig, Retort, Logger, SongService]:
        dishka_container: AsyncContainer = make_async_container(AppProvider())
        configs: AppConfig = await dishka_container.get(AppConfig)
        retort: Retort = await dishka_container.get(Retort)
        logger: Logger = await dishka_container.get(Logger)
        song_service: SongService = await dishka_container.get(SongService)
        return configs, retort, logger, song_service

    window: MainWindow = MainWindow(*loop.run_until_complete(run()))

    exit(loop.run_forever())


if __name__ == "__main__":
    main()
