class Service:
    def __init__(self) -> None:
        self._session = None

    async def get_emotes(self):
        raise NotImplementedError
