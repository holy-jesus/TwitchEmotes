from dataclasses import dataclass
from typing import overload, Literal

from TwitchEmotes.services import Service
from TwitchEmotes.services.seventv import Platform


class Config:
    service: Service

    def __init__(self, service: Service) -> None:
        self.service = service

    @overload
    def __init__(
        self,
        service: Literal[Service.SEVENTV],
        id: str,
        username: str,
        platform: str = Platform.TWITCH,
    ) -> None: ...

    @overload
    def __init__(
        self,
        service: Literal[Service.TWITCH, Service.BTTV, Service.FFZ],
        id: str,
        username: str,
    ) -> None: ...
