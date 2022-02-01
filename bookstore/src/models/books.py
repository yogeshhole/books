from typing import Optional, List

from pydantic import BaseModel, EmailStr
from src.models.common import TimestampMixIn


class Author(BaseModel):
    name: str
    email: EmailStr
    description: str

class Book(BaseModel):
    title: str
    isbn: str
    genre: str
    type: str
    publication_year: int
    price: int
    ebook: Optional[str]
    authors: List[Author]


class BookIn(TimestampMixIn):
    pass


class BookInDB(BookIn):
    id: str


class BookOut(Book):
    id: str


class BooksOut(BaseModel):
    data: List[BookOut]
