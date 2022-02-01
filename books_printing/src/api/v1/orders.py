from db.mongodb import get_database
from errors import HTTPErrorException
from fastapi import APIRouter, Depends
from loguru import logger

import src.crud.cart as carts_crud
import src.crud.orders as orders_crud
from src.models.orders import Order, Orders
from src.providers.paper_printing import place_order_to_third_party
from src.providers.shipment import create_shipment, track_shipment

orders_router = APIRouter()

NOT_FOUND = 'Requested document not found.'


@orders_router.get(path="/", response_model=Order)
async def create_order(order: Order, db: get_database = Depends()):
    try:
        if order.paper_book:
            # Place the order to third party
            shipment_id = await place_order_to_third_party(order)
        else:
            shipment_id = create_shipment(order)
    except Exception as err:
        raise HTTPErrorException(status_code=400, detail="Failed to create shipment. Please try again",
                                 err="Order not created")

    order.shipment_id = shipment_id
    try:
        db_order = await orders_crud.create_order(db, order)
    except Exception as err:
        raise HTTPErrorException(status_code=400, detail="Order not created.", error=str(err))

    # Update the cart
    try:
        cart = await carts_crud.get_cart_by_customer(db, order.customer_id)
        items = [item for item in cart.get("items") if item.get("book_id") != order.book_id]
        cart['items'] = items
        await carts_crud.update_to_the_cart(db, order.customer_id, cart)
    except Exception as err:
        logger.err(f"Cart not updated. err:{str(err)}")
    return db_order


@orders_router.get(path="/{customer_id}", response_model=Orders)
async def api_get_orders_by_customer(customer_id: str, db: get_database = Depends()):
    orders = await orders_crud.get_orders_by_customer(db, customer_id)
    if not orders:
        raise HTTPErrorException(status_code=404, detail="No orders found.", error=NOT_FOUND)
    return orders


@orders_router.get(path="/track/{shipment_id}", response_model=Orders)
async def api_track_shipment(shipment_id: str):
    return track_shipment(shipment_id=shipment_id)
