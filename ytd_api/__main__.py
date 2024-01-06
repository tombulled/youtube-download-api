import fastapi
from typing_extensions import Annotated, TypeAlias

from . import hack
from .routers import channel, search

app = fastapi.FastAPI()

app.include_router(channel.router)
app.include_router(search.router)

Id: TypeAlias = Annotated[str, fastapi.Path(alias="id")]


@app.get("/dev/playlist/{id}")
def playlist(id: Id):
    return hack.get_yt_playlist_page(id)
