from typing import Union, Dict

from bson import ObjectId
from loguru import logger
from pydantic import ValidationError


async def get_cart_by_customer(db, customer_id: str) -> Union[Dict, None]:
    fn = get_cart_by_customer.__name__

    try:
        cart_doc = await db.carts.find_one({"_id": ObjectId(customer_id)})
        return cart_doc
    except TypeError:
        return None
    except ValidationError as error:
        logger.error(f"fn: {fn} / error: {error} / Doc: {cart_doc}")
        raise error


async def update_to_the_cart(db, customer_id, cart: Dict) -> Union[Dict, None]:
    fn = get_cart_by_customer.__name__

    try:
        cart_doc = await db.carts.update_one({"_id": ObjectId(customer_id),
                                              "items": cart},
                                             upsert=True)
        return cart_doc
    except Exception as error:
        logger.error(f"fn: {fn} / error: {error} / Doc: {cart_doc}")
        raise error


async def delete_cart(db, customer_id) -> Union[Dict, None]:
    fn = get_cart_by_customer.__name__

    try:
        result = await db.carts.delete_one({"_id": ObjectId(customer_id)})
        return result
    except TypeError:
        return None
    except ValidationError as error:
        logger.error(f"fn: {fn} / error: {error} / customerr_id: {customer_id}")
        raise error
