import json
import re

from aiohttp import ClientSession

# from TwitchEmotes.services.base.emote import Emote
from TwitchEmotes.utils import get_session as _get_session
from TwitchEmotes.services.seventv.url import URL
from TwitchEmotes.exceptions import (
    ChannelNotFound as _ChannelNotFound,
    APIError as _APIError,
)


class Emote:
    def __init__(self, session: ClientSession, id: str, name: str) -> None:
        self._session = session
        self.id = id
        self.name = name

    @classmethod
    async def search_by_name(cls, name: str) -> list["Emote"]:
        session = await _get_session()
        data = json.dumps(
            [
                {
                    "operationName": "SearchEmotes",
                    "variables": {
                        "query": name,
                        "limit": 5,
                        "page": 1,
                        "sort": {"value": "popularity", "order": "DESCENDING"},
                        "filter": {
                            "category": "TOP",
                            "exact_match": False,
                            "ignore_tags": False,
                            "zero_width": False,
                            "animated": False,
                            "aspect_ratio": "",
                        },
                    },
                    "query": re.sub(
                        " +",
                        " ",
                        """query SearchEmotes($query: String!, $page: Int, $sort: Sort, $limit: Int, $filter: EmoteSearchFilter) {
                            emotes(query: $query, page: $page, sort: $sort, limit: $limit, filter: $filter) {
                                count
                                max_page
                                emotes {
                                    items {
                                        id
                                        name
                                        state
                                        trending
                                        owner {
                                            id
                                            username
                                            display_name
                                        }
                                    flags
                                    host {
                                        url
                                        files {
                                            name
                                            format
                                            width
                                            height
                                        }
                                    }
                                }
                            }
                        }""",
                    ),
                }
            ]
        )
        response = await session.post(URL.GRAPHQL, data=data)
        if response.status != 200:
            raise _APIError(f"API returned error")  # TODO
        data = response.json()
        return [
            Emote(
                session,
                emote["id"],
                emote["name"],
            )
            for emote in data["data"]["emotes"]["emotes"]["items"]
        ]
        
        

