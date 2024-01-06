from typing import Optional, Sequence

from pydantic import BaseModel

from .enums import AlbumType


class Thumbnail(BaseModel):
    url: str
    height: int
    width: int


class Album(BaseModel):
    browse_id: str
    playlist_id: str
    title: str
    type: AlbumType
    year: Optional[int]
    thumbnails: Sequence[Thumbnail]


class Channel(BaseModel):
    id: str
    title: str
    description: str
    thumbnails: Sequence[Thumbnail]
