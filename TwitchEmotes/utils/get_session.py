from aiohttp import ClientSession


_session = None


async def get_session():
    global _session

    if _session is None:
        _session = ClientSession()

    return _session
