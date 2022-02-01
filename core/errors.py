from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import Union


class HTTPErrorException(Exception):
    def __init__(self, status_code: int, detail: str = None, error: Union[str, BaseException] = None):
        self.status_code = status_code
        self.detail = detail
        self.error = error
