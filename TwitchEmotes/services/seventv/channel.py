from aiohttp import ClientSession as _ClientSession

from TwitchEmotes.utils import get_session as _get_session
from TwitchEmotes.exceptions import ChannelNotFound


_GET_BY_PLATFORM_ID = "https://7tv.io/v3/users/{platform}/{id}"


class SevenTVChannel:
    def __init__(self, session: _ClientSession) -> None:
        self._session = session

    @classmethod
    async def get_by_username(cls, username: str) -> "SevenTVChannel":
        pass

    @classmethod
    async def get_by_id(
        cls, seventv_id: str = None, twitch_id: str = None
    ) -> "SevenTVChannel":
        if seventv_id:
            await cls._get_by_seventv_id(seventv_id)
        elif twitch_id:
            await cls._get_by_twitch_id(twitch_id)
        else:
            raise ValueError(
                'At least one of "seventv_id" or "twitch_id" must be provided.'
            )

    @classmethod
    async def _get_by_seventv_id(cls, id: str) -> "SevenTVChannel":
        session = await _get_session()
        session.get("")

    @classmethod
    async def _get_by_twitch_id(cls, id: str) -> "SevenTVChannel":
        session = await _get_session()
        response = await session.get(
            _GET_BY_PLATFORM_ID.format(platform="twitch", id=id)
        )
        if response.status == 404:
            raise ChannelNotFound(
                f'The channel with ID "{id}" on the "twitch" platform was not found.'
            )
        
