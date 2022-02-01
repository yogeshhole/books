from typing import Union, Dict

from bson import ObjectId
from loguru import logger
from pydantic import ValidationError


async def get_book_by_id(db, book_id: str) -> Union[Dict, None]:
    fn = get_book_by_id.__name__

    try:
        book_doc = await db.books.find_one({"_id": ObjectId(book_id), 'deleted': {'$eq': None}})
        return book_doc
    except TypeError:
        return None
    except ValidationError as error:
        logger.error(f"fn: {fn} / error: {error} / Doc: {book_doc}")
        raise error


async def get_all_books(db) -> Union[Dict, None]:
    fn = get_all_books.__name__

    books = []
    try:
        cursor = await db.books.find({'deleted': {'$eq': None}})
        async for book in cursor.to_list(None):
            books.append(book)
    except Exception as error:
        logger.error(f"fn: {fn} / error: {error}")
        raise error
    return books
