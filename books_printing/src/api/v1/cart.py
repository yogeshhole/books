from db.mongodb import get_database
from errors import HTTPErrorException
from fastapi import APIRouter, Depends

import src.crud.cart as carts_crud
from src.models.orders import Cart

carts_router = APIRouter()

NOT_FOUND = 'Requested document not found.'


@carts_router.get(path="/", response_model=Cart)
async def api_add_to_the_cart(cart: Cart, db: get_database = Depends()):
    try:
        cart = await carts_crud.update_to_the_cart(db, cart)
    except Exception as err:
        raise HTTPErrorException(status_code=400, detail="Cart not added.", error=str(err))
    return cart


@carts_router.get(path="/{customer_id}", response_model=Cart)
async def api_get_cart_by_customer(customer_id: str, db: get_database = Depends()):
    cart = await carts_crud.get_cart_by_customer(db, customer_id)
    if not cart:
        return []
    return cart
