import requests


async def place_order_to_third_party(order):
    return requests.post("http://third-party-printing", data=order)
