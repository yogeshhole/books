from pydantic import BaseModel


class Shipper(BaseModel):
    id: str
    name: str
    phoneNumber: str

