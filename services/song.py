from core.interfaces.song_repository import SongRepository
from core.domain.song import Song


class SongService:
    def __init__(self, repo: SongRepository) -> None:
        self.repo: SongRepository = repo

    def load_song(self, file_path: str) -> Song:
        return self.repo.get_song_info(file_path)
