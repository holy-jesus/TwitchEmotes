import json
from datetime import datetime
from dataclasses import dataclass

from aiohttp import ClientSession as _ClientSession

from TwitchEmotes.utils import get_session as _get_session
from TwitchEmotes.exceptions import (
    ChannelNotFound as _ChannelNotFound,
    APIError as _APIError,
)
from TwitchEmotes.services.seventv.platform import Platform


_GET_BY_PLATFORM_ID = "https://7tv.io/v3/users/{platform}/{id}"
_GRAPHQL = "https://7tv.io/v3/gql"


@dataclass
class UserStyle:
    color: int
    paint_id: str | None


@dataclass
class UserPartial:
    id: str
    username: str
    display_name: str
    avatar_url: str
    style: UserStyle


@dataclass
class UserEditor:
    id: str
    permissions: int
    visible: bool
    user: UserPartial


class SevenTVChannel:
    def __init__(self, session: _ClientSession, data: dict) -> None:
        self._session = session
        self.id: str = data["id"]
        self.username: str = data["username"]
        self.display_name: str = data["display_name"]
        self.created_at: datetime = datetime.fromisoformat(data["created_at"])
        self.avatar_url: str = data["avatar_url"]
        self.style = UserStyle(**data["style"])
        self.biography: str = data["biography"]
        self.editors: list[UserEditor] = [UserEditor(**e) for e in data["editors"]]
        self.emote_sets: list  # TODO
        self.roles: list[str] = data["roles"]
        self.connections

    @classmethod
    async def get_by_username(
        cls,
        username: str,
    ) -> "SevenTVChannel":
        session = await _get_session()
        data = json.dumps(
            [
                {
                    "operationName": "SearchUsers",
                    "variables": {"query": username},
                    "query": """query SearchUsers($query: String!) {
                        users(query: $query) {
                            id
                            username
                            display_name
                        }
                    }""",
                }
            ]
        )
        response = await session.post(_GRAPHQL, data=data)
        if response.status != 200:
            raise _APIError(f"API returned {response.status}")  # TODO
        data = await response.json()
        for user in data[0]["data"]["users"]:
            if user["username"] == username or user["display_name"] == username:
                return await cls._get_by_seventv_id(user["id"])
        raise _ChannelNotFound(f'Channel with username "{username}" not found')

    @classmethod
    async def get_by_id(
        cls,
        platform: Platform,
        id: str,
    ) -> "SevenTVChannel":
        session = await _get_session()
        if platform not in Platform:
            raise ValueError()
        elif platform == Platform.SEVENTV:
            return await cls._get_by_seventv_id(id)
        url = _GET_BY_PLATFORM_ID.format(platform=platform, id=id)
        response = await session.get(url)
        if response.status == 404:
            raise _ChannelNotFound(
                f'The channel with ID "{id}" on the "{platform}" platform was not found.'
            )
        elif response.status != 200:
            raise _APIError(f"API returned")  # TODO

    @classmethod
    async def _get_by_seventv_id(cls, id: str) -> "SevenTVChannel":
        session = await _get_session()
        data = [
            {
                "operationName": "GetUserForUserPage",
                "variables": {"id": "01FEGJ99QR000AENY3GSAKBAHP"},
                "query": """query GetUserForUserPage($id: ObjectID!) {
                    user(id: $id) {
                        id
                        username
                        display_name
                        created_at
                        avatar_url
                        style {
                            color
                            paint_id
                            __typename
                        }
                        biography
                        editors {
                            id
                            permissions
                            visible
                            user {
                                id
                                username
                                display_name
                                avatar_url
                                style {
                                    color
                                    paint_id
                                    __typename
                                }
                            __typename
                        }
                        __typename
                    }
                    emote_sets {
                        id
                        name
                        capacity
                        owner {
                            id
                            __typename
                        }
                        __typename
                    }
                    roles
                    connections {
                        id
                        username
                        display_name
                        platform
                        linked_at
                        emote_capacity
                        emote_set_id
                        __typename
                    }
                    __typename
                }
            }""",
            }
        ]
