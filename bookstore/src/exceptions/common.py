from typing import Union


class HTTPErrorException(Exception):
    def __init__(self, status_code: int, detail: str = None, error: Union[str, BaseException] = None):
        self.status_code = status_code
        self.detail = detail
        self.error = error
