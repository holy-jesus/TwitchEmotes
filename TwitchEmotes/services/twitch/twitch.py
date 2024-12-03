from aiohttp import ClientSession

from TwitchEmotes.exceptions import ChannelNotFound
from TwitchEmotes.emotes_list import Emotes


class Twitch:
    BASE_URL = ""

    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def get_emotes(self, channel: str) -> Emotes:
        pass
