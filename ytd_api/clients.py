from typing import Final, Sequence

from innertube import InnerTube

__all__: Sequence[str] = ("WEB", "WEB_REMIX", "IOS", "IOS_MUSIC")

WEB: Final[InnerTube] = InnerTube("WEB", "2.20230728.00.00")
WEB_REMIX: Final[InnerTube] = InnerTube("WEB_REMIX", "1.20220607.03.01")
IOS: Final[InnerTube] = InnerTube("IOS", "17.14.2")
IOS_MUSIC: Final[InnerTube] = InnerTube("IOS_MUSIC", "4.16.1")
