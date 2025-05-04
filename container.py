from dishka import Provider, Scope, provide
from logging import Logger
from adaptix import Retort
from config.adapter_config import global_retort
from config.config import AppConfig
from utils.logger import setup_logger, get_logger
from repositories.file_song import FileSongRepo
from core.interfaces.song_repository import SongRepository
from services.song import SongService


class AppProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_config(self) -> AppConfig:
        return await AppConfig.load()

    @provide
    async def get_retort(self) -> Retort:
        return global_retort

    @provide
    async def setup_logger(self, config: AppConfig) -> None:
        await setup_logger(config.log_level)

    @provide
    async def get_logger(self) -> Logger:
        return await get_logger(__name__)
    
    @provide
    async def get_repo(self) -> SongRepository:
        return FileSongRepo()

    @provide
    async def get_song_service(self, song_repo: SongRepository) -> SongService:
        return SongService(song_repo)
