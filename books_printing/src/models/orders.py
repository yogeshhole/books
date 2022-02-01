from typing import List, Optional

from pydantic import BaseModel


class ShippingAddress(BaseModel):
    address: str
    pincode: str
    state: str


class Payment(BaseModel):
    amount: int
    tax: int
    shipping_charges: int
    details: dict


class Order(BaseModel):
    book_id: str
    shipment_id: Optional[str]
    address: ShippingAddress
    date: int
    customer_id: str
    paper_book: bool
    ebook: bool
    payment_details: Payment
    quantity: int


class Orders(BaseModel):
    orders: List[Order]


class CartItem(BaseModel):
    book_id: str
    quantity: int
    price: int


class Cart(BaseModel):
    items: List[CartItem]
