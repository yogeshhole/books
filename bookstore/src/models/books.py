from typing import Optional, List

from pydantic import BaseModel

from src.models.common import TimestampMixIn


class Book(BaseModel):
    title: str
    isbn: str
    genre: str
    type: int
    publication_year: int
    price: int
    ebook: Optional[str]


class BookIn(TimestampMixIn):
    pass


class BookInUpdate(BaseModel):
    title: Optional[str]
    genre: Optional[str]
    type: Optional[str]
    publication_year: Optional[int]
    price: Optional[int]
    ebook: Optional[str]


class BookInDB(BookIn):
    id: str


class BookOut(Book):
    id: str


class BooksOut(BaseModel):
    data: List[BookOut]
