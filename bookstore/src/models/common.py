from typing import Optional

from pydantic import BaseModel


class TimestampMixIn(BaseModel):
    created: Optional[int]
    updated: Optional[int]
