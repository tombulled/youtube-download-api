from enum import Enum


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class AlbumType(StrEnum):
    ALBUM: str = "Album"
    EP: str = "EP"
    SINGLE: str = "Single"
    PLAYLIST: str = "Playlist"
