from pymongo import IndexModel

from db.mongodb import get_database


async def create_indexes():
    idx_books = [
        IndexModel('customer_id', unique=True),
        IndexModel('book_id', unique=True),
    ]

    db = await get_database()
    await db.users.create_indexes(idx_books)
