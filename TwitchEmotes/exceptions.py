class TwitchEmotesException(Exception):
    pass


class ChannelNotFound(TwitchEmotesException):
    pass


class APIError(TwitchEmotesException):
    pass