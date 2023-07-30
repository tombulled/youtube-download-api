from pydantic import BaseModel
from typing import Sequence

from .enums import AlbumType


class Thumbnail(BaseModel):
    url: str
    height: str
    width: str


class Album(BaseModel):
    browse_id: str
    playlist_id: str
    title: str
    type: AlbumType
    year: int
    thumbnails: Sequence[Thumbnail]


class Channel(BaseModel):
    id: str
    title: str
    description: str
    thumbnails: Sequence[Thumbnail]
