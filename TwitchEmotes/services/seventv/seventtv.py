from typing import overload

from TwitchEmotes.services.seventv.channel import Channel


class SevenTV:
    @classmethod
    async def get_emote(cls, id: str):
        pass

    @classmethod
    async def get_emote_set(cls, id: str):
        pass

    @classmethod
    async def search_emote(cls, text: str):
        pass

    @classmethod
    async def get_channels_sets(cls, *, seventv_id: str = None, username: str = None):
        if not seventv_id and not username:
            raise ValueError("")  # TODO
        elif seventv_id:
            pass
        elif username:
            Channel

    @overload
    @classmethod
    async def get_channels_sets(cls, *, id: str): ...

    @overload
    @classmethod
    async def get_channels_sets(cls, *, username: str): ...
