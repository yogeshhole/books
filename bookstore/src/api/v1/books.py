from fastapi import APIRouter, Depends

import src.crud.books as books_crud
from db.mongodb import get_database
from src.exceptions.common import HTTPErrorException
from src.models.books import BookOut, BooksOut

books_router = APIRouter()

NOT_FOUND = 'Requested document not found.'


@books_router.get(path="/", response_model=BooksOut)
async def api_get_all_books(db: get_database = Depends()):
    book = await books_crud.get_all_books(db)
    if not book:
        raise HTTPErrorException(status_code=404, detail=f"Books not found")
    return book


@books_router.get(path="/{book_id}", response_model=BookOut)
async def api_get_book_by_id(book_id: str, db: get_database = Depends()):
    book = await books_crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPErrorException(status_code=404, detail=f"Book not found for book_id {book_id}")
    return book
