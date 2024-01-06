import random
import time
from typing import Sequence

import rich

from ytd_api.api import get_channel, get_channel_albums
from ytd_api.models import Album, Channel


def delay() -> None:
    timeout: float = random.randint(2000, 5000) / 1000

    time.sleep(timeout)


channel_id: str = "UC8Yu1_yfN5qPh601Y4btsYw"  # Arctic Monkeys

channel: Channel = get_channel(channel_id)

rich.print(f"Albums of {channel.title!r}:")

delay()

albums: Sequence[Album] = get_channel_albums(channel_id)

album: Album
for album in albums:
    rich.print(
        f"\t {album.playlist_id} | {album.title!r} ({album.type.value}, {album.year})"
    )
