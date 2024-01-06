from pathlib import Path
from typing import Optional, Sequence

import rich

import ytd_api
from ytd_api.hack import (
    PlaylistPage,
    PlaylistSong,
    delay,
    download,
    get_channel_albums,
    get_video_stream_url,
    get_yt_playlist_page,
)

"""
TODO:
    1. Support downloading age-gated content, e.g. https://www.youtube.com/watch?v=nLfhkoB4D5k&list=OLAK5uy_nabdgZPZ32q9j3ROBMe0o_xZZiBnUmmAE&index=11

TODO:
    (x) Air Review
    (x) alt-J
    (x) Arctic Monkeys
    (x) AWOLNATION
    Bad Suns
    Bag Raiders
    (x) Band of Horses
    Bastille
    Bear's Den
    Bleachers
    Blossoms
    Borns
    Cage the Elephant
    Circa Waves
    Daft Punk
    Death Cab for Cutie
    Declan McKenna
    ...
    (x) Easy Life
    ...
    Red Hot Chilli Peppers
    ...
    (x) Rex Orange County
    ...
    (x) Still Woozy <--
    ...
    (x) The Lumineers
"""

channel_id: str = input("Channel ID: ")

print()

delay()

albums: Sequence[ytd_api.models.Album] = get_channel_albums(channel_id)

playlist_ids: Sequence[str] = [album.playlist_id for album in albums]

playlist_id: str
for playlist_id in playlist_ids:
    delay()

    playlist: PlaylistPage = get_yt_playlist_page(playlist_id)

    rich.print(f"Downloading: {playlist.name!r} by {playlist.channel_name!r}")

    music_dir: Path = Path.home() / "Music"

    album_dir: Path = music_dir / Path(f"{playlist.channel_name} - {playlist.name}")

    if not album_dir.exists():
        album_dir.mkdir()

    album_thumbnail_path: Path = album_dir.joinpath("thumbnail.jpg")

    if not album_thumbnail_path.exists():
        download(playlist.thumbnail, album_thumbnail_path)

    total_tracks: int = len(playlist.songs)

    index: int
    track: PlaylistSong
    for index, track in enumerate(playlist.songs):
        safe_track_name: str = track.name.translate(
            str.maketrans(
                {
                    char: "_"
                    for char in ("/", "<", ">", ":", '"', "/", "\\", "|", "?", "*")
                }
            )
        )
        track_path: Path = album_dir.joinpath(
            f"{str(index+1).zfill(2)} - {safe_track_name}.m4a"
        )

        rich.print(
            f"\t ({str(index+1).zfill(2)}/{str(total_tracks).zfill(2)}) {track.name!r} [{track.id!r}]"
        )

        if track_path.exists():
            rich.print("\t\t (already downloaded, skipping.)")
            continue

        delay()

        try:
            track_url: Optional[str] = get_video_stream_url(track.id)
        except Exception as error:
            rich.print(f"\t\t ERROR: {error}")
            continue

        if track_url is None:
            continue

        delay()

        import os

        os.system(f'wget -q "{track_url}" -O "{track_path}"')
