from os.path import splitext, basename
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, APIC  # noqa: F401
from core.domain.song import Song
from core.interfaces.song_repository import SongRepository


class FileSongRepo(SongRepository):
    def get_song_info(self, file_path: str):
        audio: MP3 = MP3(file_path, ID3=ID3)

        tags = audio.tags
        if tags is None:
            title: str = splitext(basename(file_path))[0]
            artist: str = "Неизвестно"
            album: str = "Неизвестно"
        else:
            title: str = str(tags.get("TIT2", "Неизвестно"))
            artist: str = str(tags.get("TPE1", "Неизвестно"))
            album: str = str(tags.get("TALB", "Неизвестно"))
        duration = int(audio.info.length)
        return Song(title=title, artist=artist, album=album, duration=duration, path=file_path)
