from pymongo import IndexModel

from db.mongodb import get_database


async def create_indexes():
    idx_books = [
        IndexModel('isbn', unique=True),
        IndexModel('deleted'),
    ]

    db = await get_database()
    await db.users.create_indexes(idx_books)
