from typing import Sequence
from typing_extensions import Annotated, TypeAlias

import fastapi
from .. import api

__all__ = ("router",)

Query: TypeAlias = Annotated[str, fastapi.Query(alias="q")]

router = fastapi.APIRouter()


@router.get("/search/suggest")
def search_suggest(query: Query) -> Sequence[str]:
    return api.yt_complete_search(query)
