import re
import json
from pprint import pprint

from aiohttp import ClientSession

from TwitchEmotes.services.base.emote_set import EmoteSet
from TwitchEmotes.services.seventv.url import URL
from TwitchEmotes.services.seventv.emote import Emote


class EmoteSet(EmoteSet):
    def __init__(
        self, session: ClientSession, id: str, owner_id: str, default: bool
    ) -> None:
        self._session: ClientSession = session
        self.id: str = id
        self.owner_id: str = owner_id
        self.default: bool = default

    async def get_emotes(self):
        data = json.dumps(
            [
                {
                    "operationName": "GetEmoteSet",
                    "variables": {"id": self.id},
                    "query": re.sub(
                        " +",
                        " ",
                        """query GetEmoteSet($id: ObjectID!, $formats: [ImageFormat!]) {
                            emoteSet(id: $id) {
                                id
                                name
                                emotes {
                                    data {
                                        id
                                        name
                                        host {
                                            url
                                            files(formats: $formats) {
                                                name
                                                format
                                            }
                                        }
                                    }
                                }
                                owner {
                                    id
                                    username
                                    display_name
                                }
                            }
                        }""",
                    ),
                }
            ]
        )
        response = await self._session.post(URL.GRAPHQL, data=data)
        data = await response.json()
        pprint(data[0]["data"]["emoteSet"]["emotes"][0])
        emote = data[0]["data"]["emoteSet"]["emotes"][0]
        emotes = []
        url = "https:" + emote["data"]["host"]["url"]
        for file in emote["data"]["host"]["files"]:
            emotes.append(
                Emote()
            )
