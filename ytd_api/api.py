from typing import Any, Mapping, Optional, Sequence

import httpx

from . import utils
from .clients import WEB_REMIX
from .enums import AlbumType
from .models import Album, Channel, Thumbnail

"""
/search?q={query}
/search/channels?q={query} OR /search?q={query}&type={channel}
/search/suggestions?q={query}

/channel/{id}
/channel/{id}/albums
/channel/{id}/singles
/channel/{id}/songs
/channel/{id}/videos
/channel/{id}/featured/playlists
/channel/{id}/featured/channels

/playlist/{id}

/album/{id}

/video/{id}

/explore
/explore/new-releases
/explore/charts
/explore/moods-and-genres
/explore/podcasts
"""


def yt_complete_search(query: str, /) -> Sequence[str]:
    r = httpx.get(
        "https://suggestqueries-clients6.youtube.com/complete/search",
        params={
            "client": "youtube",
            "hl": "en-gb",
            "gl": "gb",
            "ds": "yt",
            "q": query,
            "xhr": "t",
            "hjson": "t",
        },
    )

    return [suggestion[0] for suggestion in r.json()[1]]


# /channel/{id}
def get_channel(channel_id: str, /) -> Channel:
    data: dict = WEB_REMIX.browse(channel_id)

    music_immersive_header_renderer: Mapping[str, Any] = data["header"][
        "musicImmersiveHeaderRenderer"
    ]

    return Channel(
        id=channel_id,
        title=utils.text(music_immersive_header_renderer["title"]),
        description=utils.text(music_immersive_header_renderer["description"]),
        thumbnails=[
            Thumbnail(
                url=thumbnail["url"],
                width=thumbnail["width"],
                height=thumbnail["height"],
            )
            for thumbnail in music_immersive_header_renderer["thumbnail"][
                "musicThumbnailRenderer"
            ]["thumbnail"]["thumbnails"]
        ],
    )


# /channel/{id}/songs
def get_channel_songs(channel_id: str, /):
    # data: dict = WEB_REMIX.browse(channel_id)

    # contents: Sequence[Mapping[str, Mapping[str, Any]]] = data["contents"][
    #     "singleColumnBrowseResultsRenderer"
    # ]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"]

    # contents_map: Mapping[str, Sequence[Mapping[str, Any]]] = utils.flatten(contents)

    # music_shelf_renderer: Mapping[str, Any] = data["musicShelfRenderer"]

    ...


# /channel/{id}/albums
def get_channel_albums(channel_id: str, /):
    data: dict = WEB_REMIX.browse(channel_id)

    contents: Sequence[Mapping[str, Mapping[str, Any]]] = data["contents"][
        "singleColumnBrowseResultsRenderer"
    ]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"]

    contents_map: Mapping[str, Sequence[Mapping[str, Any]]] = utils.flatten(contents)

    music_carousel_shelf_renderers: Sequence[Mapping[str, Any]] = contents_map[
        "musicCarouselShelfRenderer"
    ]

    music_carousel_shelf_renderer: Mapping[str, Any] = utils.filter_one(
        music_carousel_shelf_renderers,
        lambda music_carousel_shelf_renderer: utils.text(
            music_carousel_shelf_renderer["header"][
                "musicCarouselShelfBasicHeaderRenderer"
            ]["title"]
        )
        == "Albums",
    )

    music_carousel_shelf_basic_header_renderer = music_carousel_shelf_renderer[
        "header"
    ]["musicCarouselShelfBasicHeaderRenderer"]

    # TODO: Use me to get page with all albums on
    more_button_browse_params: Optional[str] = (
        music_carousel_shelf_basic_header_renderer["moreContentButton"][
            "buttonRenderer"
        ]["navigationEndpoint"]["browseEndpoint"]["params"]
        if "moreContentButton" in music_carousel_shelf_basic_header_renderer
        else None
    )

    music_two_row_item_renderers: Sequence[Mapping[str, Any]] = utils.flatten(
        music_carousel_shelf_renderer["contents"]
    )["musicTwoRowItemRenderer"]

    return [
        Album.parse_obj(
            dict(
                browse_id=music_two_row_item_renderer["navigationEndpoint"][
                    "browseEndpoint"
                ]["browseId"],
                playlist_id=music_two_row_item_renderer["thumbnailOverlay"][
                    "musicItemThumbnailOverlayRenderer"
                ]["content"]["musicPlayButtonRenderer"]["playNavigationEndpoint"][
                    "watchPlaylistEndpoint"
                ][
                    "playlistId"
                ],
                title=utils.text(music_two_row_item_renderer["title"]),
                type=utils.text_all(music_two_row_item_renderer["subtitle"])[0],
                year=utils.text_all(music_two_row_item_renderer["subtitle"])[-1],
                thumbnails=music_two_row_item_renderer["thumbnailRenderer"][
                    "musicThumbnailRenderer"
                ]["thumbnail"]["thumbnails"],
            )
        )
        for music_two_row_item_renderer in music_two_row_item_renderers
    ]


# /channel/{id}/singles
def get_channel_singles(channel_id: str, /):
    data: dict = WEB_REMIX.browse(channel_id)

    contents: Sequence[Mapping[str, Mapping[str, Any]]] = data["contents"][
        "singleColumnBrowseResultsRenderer"
    ]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"]

    contents_map: Mapping[str, Sequence[Mapping[str, Any]]] = utils.flatten(contents)

    music_carousel_shelf_renderers: Sequence[Mapping[str, Any]] = contents_map[
        "musicCarouselShelfRenderer"
    ]

    music_carousel_shelf_renderer: Mapping[str, Any] = utils.filter_one(
        music_carousel_shelf_renderers,
        lambda music_carousel_shelf_renderer: utils.text(
            music_carousel_shelf_renderer["header"][
                "musicCarouselShelfBasicHeaderRenderer"
            ]["title"]
        )
        == "Singles",
    )

    # TODO: Use me to get page with all singles on
    more_button_browse_params: str = music_carousel_shelf_renderer["header"][
        "musicCarouselShelfBasicHeaderRenderer"
    ]["moreContentButton"]["buttonRenderer"]["navigationEndpoint"]["browseEndpoint"][
        "params"
    ]

    music_two_row_item_renderers: Sequence[Mapping[str, Any]] = utils.flatten(
        music_carousel_shelf_renderer["contents"]
    )["musicTwoRowItemRenderer"]

    return [
        Album.parse_obj(
            dict(
                browse_id=music_two_row_item_renderer["navigationEndpoint"][
                    "browseEndpoint"
                ]["browseId"],
                playlist_id=music_two_row_item_renderer["thumbnailOverlay"][
                    "musicItemThumbnailOverlayRenderer"
                ]["content"]["musicPlayButtonRenderer"]["playNavigationEndpoint"][
                    "watchPlaylistEndpoint"
                ][
                    "playlistId"
                ],
                title=utils.text(music_two_row_item_renderer["title"]),
                type=AlbumType.SINGLE,
                year=utils.text_all(music_two_row_item_renderer["subtitle"])[-1],
                thumbnails=music_two_row_item_renderer["thumbnailRenderer"][
                    "musicThumbnailRenderer"
                ]["thumbnail"]["thumbnails"],
            )
        )
        for music_two_row_item_renderer in music_two_row_item_renderers
    ]


# /channel/{id}/videos
def get_channel_videos(channel_id: str, /):
    ...


# /channel/{id}/featured/playlists
def get_channel_featured_playlists(channel_id: str, /):
    data: dict = WEB_REMIX.browse(channel_id)

    contents: Sequence[Mapping[str, Mapping[str, Any]]] = data["contents"][
        "singleColumnBrowseResultsRenderer"
    ]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]["contents"]

    contents_map: Mapping[str, Sequence[Mapping[str, Any]]] = utils.flatten(contents)

    music_carousel_shelf_renderers: Sequence[Mapping[str, Any]] = contents_map[
        "musicCarouselShelfRenderer"
    ]

    music_carousel_shelf_renderer: Mapping[str, Any] = utils.filter_one(
        music_carousel_shelf_renderers,
        lambda music_carousel_shelf_renderer: utils.text(
            music_carousel_shelf_renderer["header"][
                "musicCarouselShelfBasicHeaderRenderer"
            ]["title"]
        )
        == "Featured on",
    )

    music_two_row_item_renderers: Sequence[Mapping[str, Any]] = utils.flatten(
        music_carousel_shelf_renderer["contents"]
    )["musicTwoRowItemRenderer"]

    return [
        Album.parse_obj(
            dict(
                browse_id=music_two_row_item_renderer["navigationEndpoint"][
                    "browseEndpoint"
                ]["browseId"],
                playlist_id=music_two_row_item_renderer["thumbnailOverlay"][
                    "musicItemThumbnailOverlayRenderer"
                ]["content"]["musicPlayButtonRenderer"]["playNavigationEndpoint"][
                    "watchPlaylistEndpoint"
                ][
                    "playlistId"
                ],
                title=utils.text(music_two_row_item_renderer["title"]),
                type=utils.text_all(music_two_row_item_renderer["subtitle"])[0],
                year=None,
                thumbnails=music_two_row_item_renderer["thumbnailRenderer"][
                    "musicThumbnailRenderer"
                ]["thumbnail"]["thumbnails"],
            )
        )
        for music_two_row_item_renderer in music_two_row_item_renderers
    ]


# /channel/{id}/featured/channels
def get_channel_similar_channels(channel_id: str, /):
    ...
