from typing import Union, Dict

from bson import ObjectId
from loguru import logger


async def get_orders_by_customer(db, customer_id: str) -> Union[Dict, None]:
    fn = get_orders_by_customer.__name__

    orders = []
    try:
        cursor = db.orders.find({"_id": ObjectId(customer_id)})
        for doc in await cursor.to_list(None):
            orders.append(doc)
    except Exception as error:
        logger.error(f"fn: {fn} / error: {error} / customer_id: {customer_id}")
        raise error
    return orders


async def create_order(db, order: Dict) -> Union[Dict, None]:
    fn = create_order.__name__

    try:
        result = await db.carts.insert_one({**order})
        return result
    except Exception as error:
        logger.error(f"fn: {fn} / error: {error} / Doc: {order}")
        raise error
