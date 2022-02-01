import random
import string

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse


def create_aliased_response(model: BaseModel) -> JSONResponse:
    """convert response to JSON compatible format. (ie: Pydantic model to a dict, and datetime to a str)
    The result of calling it is something that can be encoded with the Python standard json.dumps()
    will also covert Pydantic aliases:  name: str = Field(None, alias='ActorName')"""
    return JSONResponse(content=jsonable_encoder(model, by_alias=True))


def generate_invite_code(string_length=8):
    """Generate a random string of letters and digits for the account invite code"""
    code = string.ascii_letters + string.digits
    return ''.join(random.choice(code) for i in range(string_length))
