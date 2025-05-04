from abc import ABC, abstractmethod
from core.domain.song import Song


class SongRepository(ABC):
    @abstractmethod
    def get_song_info(self, file_path: str) -> Song: ...
