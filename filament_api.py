import uuid
import requests
from web3 import Web3
from eth_account.messages import encode_defunct

from constants import (
    ACOUNT,
    API_BASE_URL,
    EXCHANGE_URL,
    HEADERS,
    INDEX_TOKEN,
    SIGNING_KEY,
)


# Function to handle order signature
def handle_order_signature(order_id, signature_key):
    print(
        f">>> @handle_order_signature orderId: {order_id}, signature_key: {signature_key}"
    )
    w3 = Web3()  # Initialize web3
    signer = w3.eth.account.from_key(signature_key)  # Create account from private key
    # print(">>> @handle_order_signature -> signer : ", signer)
    msghash = encode_defunct(text=order_id)
    # print(">>> @handle_order_signature -> msghash : ", msghash)
    order_signature = signer.sign_message(msghash).signature.hex()  # Sign the order ID
    return order_signature


# REST API Calls
# Function to get order book
def get_order_book():
    url = f"{API_BASE_URL}/filament/api/v1/assets"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        print(f">>> Order Book: {response.json()}")
    else:
        print(f">>> Error fetching order book: {response.text}")


# Function to submit limit order
def submit_limit_order(
    index_token=INDEX_TOKEN, size=100, leverage=1.1, reduceOnly=False
):
    order_id = str(uuid.uuid4()).replace("-", "")  # Generating a unique order ID
    order_signature = handle_order_signature(
        order_id, SIGNING_KEY
    )  # Generate a signature for the order

    # Construct the payload object
    payload = {
        "type": "order",
        "referralCode": None,
        "orders": [
            {
                "account": ACOUNT.lower(),
                "indexToken": index_token,
                "isBuy": True,
                "size": size,  # 100,
                "leverage": leverage,  # 1.1,
                "reduceOnly": reduceOnly,  # False,
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

    try:
        response = requests.post(EXCHANGE_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # Check if request was successful
        print(
            ">>> RESPONSE @ submit_order : ", response.json()
        )  # Print the response data
    except requests.exceptions.RequestException as e:
        print(f">>> ERROR @ submit_order : {e}")

    return order_id


# Function to submit limit order
def submit_market_order(
    index_token=INDEX_TOKEN, size=100, leverage=1.1, reduceOnly=False
):
    order_id = str(uuid.uuid4()).replace("-", "")  # Generating a unique order ID
    order_signature = handle_order_signature(
        order_id, SIGNING_KEY
    )  # Generate a signature for the order

    # Construct the payload object
    payload = {
        "type": "order",
        "referralCode": "null",
        "orders": [
            {
                "account": ACOUNT.lower(),
                "indexToken": index_token,
                "isBuy": "true",
                "size": size,  # 22,
                "leverage": leverage,  # 1.1,
                "reduceOnly": reduceOnly,  # false,
                "orderId": order_id,
                "signature": order_signature,
                "orderType": {
                    "type": "trigger",
                    "trigger": {"isMarket": "true", "slippage": 5},
                },
            }
        ],
    }

    print(f">>> payload: \n{payload}")

    try:
        response = requests.post(EXCHANGE_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # Check if request was successful
        print(
            ">>> RESPONSE @ submit_order : ", response.json()
        )  # Print the response data
    except requests.exceptions.RequestException as e:
        print(f">>> ERROR @ submit_order : {e}")

    return order_id


def cancel_order(orderId):
    payload = {
        "type": "cancel",
        "cancels": [
            {
                "account": ACOUNT.lower(),
                "orderId": orderId,  # Cancel each order individually
                "signature": SIGNING_KEY,
            }
        ],
    }

    response = requests.post(EXCHANGE_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print(f">>> RESPONSE @ cancel_order : {response.json()}")
    else:
        print(f">>> ERROR @ cancel_order: {response.text}")
