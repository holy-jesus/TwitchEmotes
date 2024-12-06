import json
import re

from TwitchEmotes.utils import get_session as _get_session
from TwitchEmotes.exceptions import (
    ChannelNotFound as _ChannelNotFound,
    APIError as _APIError,
)
from TwitchEmotes.services.seventv.platform import Platform
from TwitchEmotes.services.seventv.emote_set import EmoteSet
from TwitchEmotes.services.seventv.url import URL


class Channel:
    @classmethod
    async def get_by_username(cls, username: str):
        session = await _get_session()
        data = json.dumps(
            [
                {
                    "operationName": "SearchUsers",
                    "variables": {"query": username},
                    "query": re.sub(
                        " +",
                        " ",
                        """query SearchUsers($query: String!) {
                            users(query: $query) {
                                id
                                username
                                display_name
                            }
                        }""",
                    ),
                }
            ]
        )
        response = await session.post(URL.GRAPHQL, data=data)
        if response.status != 200:
            raise _APIError(f"API returned {response.status}")  # TODO
        data = await response.json()
        for user in data[0]["data"]["users"]:
            if user["username"] == username or user["display_name"] == username:
                return await cls._get_by_seventv_id(user["id"])
        raise _ChannelNotFound(f'Channel with username "{username}" not found')

    @classmethod
    async def get_by_id(cls, platform: Platform, id: str):
        session = await _get_session()
        if platform not in Platform:
            raise ValueError("")  # TODO
        elif platform == Platform.SEVENTV:
            return await cls._get_by_seventv_id(id)
        url = URL.GET_USER_BY_PLATFORM_ID.format(platform=platform, id=id)
        response = await session.get(url)
        if response.status == 404:
            raise _ChannelNotFound(
                f'The channel with ID "{id}" on the "{platform}" platform was not found.'
            )
        elif response.status != 200:
            raise _APIError(f"API returned error")  # TODO

    @classmethod
    async def _get_by_seventv_id(cls, id: str):
        session = await _get_session()
        data = json.dumps(
            [
                {
                    "operationName": "GetUserForUserPage",
                    "variables": {"id": id},
                    "query": re.sub(
                        " +",
                        " ",
                        """query GetUserForUserPage($id: ObjectID!) {
                                user(id: $id) {
                                    id
                                emote_sets {
                                    id
                                    owner {
                                        id
                                    }
                                }
                                connections {
                                    platform
                                    emote_set_id
                                }
                            }
                        }""",
                    ),
                }
            ]
        )
        response = await session.post(URL.GRAPHQL, data=data)
        if response.status == 404:
            raise _ChannelNotFound(f'The channel with ID "{id}" was not found.')
        elif response.status != 200:
            raise _APIError(f"API returned error")  # TODO
        data = await response.json()
        default_set_id = data[0]["data"]["user"]["connections"][0]["emote_set_id"]
        return tuple(
            EmoteSet(
                session,
                emote_set["id"],
                emote_set["owner"]["id"],
                emote_set["id"] == default_set_id,
            )
            for emote_set in data[0]["data"]["user"]["emote_sets"]
        )
