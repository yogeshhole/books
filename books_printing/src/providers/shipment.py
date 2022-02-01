import requests
import uuid
def create_shipment(order):
    # Send request to third party if needed
    # Generate the shipment ID
    return uuid.uuid4().hex


def track_shipment(shipment_id):

    # requests.get(f"https://track-shipment/{shipment_id}")

    # return random string for testing
    return uuid.uuid4().hex