from enum import StrEnum as _StrEnum


class Service(_StrEnum):
    SEVENTV = "seventv"
    BTTV = "bttv"
    FFZ = "ffz"
    TWITCH = "twitch"


from ..config import Config
