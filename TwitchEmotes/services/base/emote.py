class Emote:
    BASE_URL: str

    id: str
    name: str
    url: str

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name
