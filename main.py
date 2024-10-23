import json
import time
import uuid
import requests
from web3 import Web3
from eth_account.messages import encode_defunct
from websocket import create_connection
import webstompy

from constants import ACOUNT, API_BASE_URL, HEADERS, INDEX_TOKEN, SIGNING_KEY, WEB_SOCKET_URL

def get_socket_server(server_url):
    url = server_url + "/websocket"
    if url[:5] == "https":
        url = "wss" + url[5:]
    else:
        url = "ws" + url[4:]

    print(">>> web socket url : ", url)
    return url


# Custom listener class for STOMP connection
class MyStompListener(webstompy.StompListener):

    def on_message(self, frame):
        print(f">>> Message received: {frame.payload}")


def connect_to_websocket():

    # Create the WebSocket connection
    ws_echo = create_connection(get_socket_server(WEB_SOCKET_URL))
    connection = webstompy.StompConnection(connector=ws_echo)

    # Create and add the custom listener
    connection.add_listener(MyStompListener())
    connection.connect(login="guest", passcode="guest")

    # Send initialization message after connection is established
    connection.send(message=INDEX_TOKEN, destination="/app/init")

    # Subscribe to a topic to receive messages
    # connection.subscribe(destination="/topic/orderBookState", id="0")
    connection.subscribe(destination="/topic/livefeed", id="0")

    return connection


# Function to handle heartbeat
def handle_heartbeat(conn):
    while True:
        try:
            if not conn.is_connected():
                print(">>> Reconnecting...")
                connect_to_websocket()
            time.sleep(10)  # Ping every 10 seconds
        except Exception as e:
            print(f"Heartbeat error: {e}")


# Function to handle order signature
def handle_order_signature(order_id, signature_key):
    print(
        f">>> @handle_order_signature orderId: {order_id}, signature_key: {signature_key}"
    )
    w3 = Web3()  # Initialize web3
    signer = w3.eth.account.from_key(signature_key)  # Create account from private key
    print(">>> >>> @handle_order_signature -> signer : ", signer)
    msghash = encode_defunct(text=order_id)
    print(">>> >>> @handle_order_signature -> msghash : ", msghash)
    order_signature = signer.sign_message(msghash).signature.hex()  # Sign the order ID
    return order_signature


# Example usage:
# order_signature = handle_order_signature("order123", "your_private_key_here")


# REST API Calls
def get_order_book():
    url = f"{API_BASE_URL}/filament/api/v1/assets"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        print(f">>> Order Book: {response.json()}")
    else:
        print(f">>> Error fetching order book: {response.text}")


def submit_batch_orders():
    url = f"{API_BASE_URL}/filament/api/v1/exchange"

    # Generate a unique order ID using uuid
    order_id = str(uuid.uuid4()).replace("-", "")
    # Sign the order ID using the provided signing key
    order_signature = handle_order_signature(order_id, SIGNING_KEY)
    print(">>> >>> @submit_batch_orders -> order_signature : ", order_signature)

    # Construct the payload dictionary
    payload = {
        "type": "order",
        "referralCode": None,
        "orders": [
            {
                "account": ACOUNT.lower(),
                "indexToken": INDEX_TOKEN,
                "isBuy": True,
                "size": 100,
                "leverage": 1.1,
                "reduceOnly": False,
                "orderId": order_id,
                "signature": order_signature,
                "orderType": {
                    "type": "trigger",
                    "trigger": {"isMarket": True, "slippage": 1},
                },
            }
        ],
    }

    print(f">>> payload: \n{payload}")

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print(f">>> Batch Orders Submitted: \n{response.json()}")
    else:
        print(f">>> Error submitting batch orders: \n{response.text}")


def cancel_all_orders():
    url = f"{API_BASE_URL}/filament/api/v1/exchange"
    payload = {
        "type": "cancel",
        "cancels": [
            {
                "account": ACOUNT.lower(),
                "orderId": f"",  # Cancel each order individually
                "signature": SIGNING_KEY,
            }
        ],
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print(f">>> All Orders Cancelled: {response.json()}")
    else:
        print(f">>> Error cancelling orders: {response.text}")


# Main Function to Manage WebSocket and REST Calls
def main():
    # Connect and subscribe to the WebSocket feed
    connect_to_websocket()
    # Start the heartbeat process to ensure the connection stays alive
    # handle_heartbeat(conn)

    # Wait for WebSocket to establish
    time.sleep(5)

    # # Fetch Order Book using REST API (public)
    # print("\n>>> get order book\n")
    # get_order_book()

    # # Submit Batch Orders (private)
    # print("\n>>> submit batch orders\n")
    # submit_batch_orders()

    # # Cancel all orders (private)
    # time.sleep(10)  # Wait for some time before cancelling
    # print("\n>>> cancel all orders\n")
    # cancel_all_orders()

    # Keep script running to maintain WebSocket connection
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
