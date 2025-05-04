from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Song:
    title: str
    artist: str
    duration: int
    path: str
    album: Optional[str] = None
