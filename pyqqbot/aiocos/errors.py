import re

__all__ = ['CosClientError', 'CosServiceError']


class CosClientError(Exception):
    pass


class CosServiceError(Exception):
    def __init__(self, msg, status):
        self._msg = msg
        info = re.compile(r'<(\w+)>([^<]+)</\1>').findall(msg)
        self._info = dict(info)
        self._http_status = status
