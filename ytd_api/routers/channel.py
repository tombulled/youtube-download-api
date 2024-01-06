from typing_extensions import Annotated, TypeAlias

from fastapi import APIRouter, Path
from .. import api
from ..models import Channel

__all__ = ("router",)

Id: TypeAlias = Annotated[str, Path(alias="id")]

router = APIRouter()


@router.get("/channel/{id}")
def channel(id: Id) -> Channel:
    return api.get_channel(id)


@router.get("/channel/{id}/albums")
def channel_albums(id: Id):
    return api.get_channel_albums(id)


@router.get("/channel/{id}/singles")
def channel_singles(id: Id):
    return api.get_channel_singles(id)


@router.get("/channel/{id}/songs")
def channel_songs(id: Id):
    return "Not implemented"

@router.get("/channel/{id}/videos")
def channel_videos(id: Id):
    return "Not implemented"


@router.get("/channel/{id}/featured/playlists")
def channel_featured_playlists(id: Id):
    return "Not implemented"


@router.get("/channel/{id}/featured/channels")
def channel_featured_channels(id: Id):
    return "Not implemented"
