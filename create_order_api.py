import uuid
import requests
from web3 import Web3
from eth_account.messages import encode_defunct

# Constants for API
API_BASE_URL = "https://orderbook.filament.finance/sei"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjB4NmI4OWRlYThiM2NhYjZhNWQzMTRlNWFjMzUxZjE5MjJlNmVlMzQzMiIsInN1YiI6IjB4NmI4OWRlYThiM2NhYjZhNWQzMTRlNWFjMzUxZjE5MjJlNmVlMzQzMiIsImlhdCI6MTcyOTAzNjgwMCwiZXhwIjoxNzI5Njg2NDU1fQ.tYO5UFjLHaUKa2s3TZtKffTT9Qvsv7EDNYQSdTCqGHM"  # Use your token
SIGNING_KEY = "0x7e0168eeabfa46d615112e2e689dfb62d73f9066699bb6a3ecef1242e12f438c"
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}
INDEX_TOKEN = "BTC"  # BTC Index Token as example
account = "0x6b89dEa8b3CAb6A5d314e5aC351f1922e6Ee3432"


# Function to handle order signature
def handle_order_signature(order_id, signature_key):
    print(f">>> @handle_order_signature orderId: {order_id}, signature_key: {signature_key}")
    w3 = Web3()  # Initialize web3
    signer = w3.eth.account.from_key(signature_key)  # Create account from private key
    print(">>> @handle_order_signature -> signer : ", signer)
    msghash = encode_defunct(text=order_id)
    print(">>> @handle_order_signature -> msghash : ", msghash)
    order_signature = signer.sign_message(msghash).signature.hex()  # Sign the order ID
    return order_signature


# Function to submit orders
def submit_orders():
    url = f"{API_BASE_URL}/filament/api/v1/exchange"

    order_id = str(uuid.uuid4()).replace("-", "")  # Generating a unique order ID
    order_signature = handle_order_signature(order_id, SIGNING_KEY)  # Generate a signature for the order
    print(f">>> orderSignature: {order_signature}")

    # Construct the payload object
    payload = {
        "type": "order",
        "referralCode": None,
        "orders": [
            {
                "account": account.lower(),
                "indexToken": INDEX_TOKEN,
                "isBuy": True,
                "size": 100,
                "leverage": 1.1,
                "reduceOnly": False,
                "orderId": order_id,
                "signature": order_signature,
                "orderType": {
                    "type": "trigger",
                    "trigger": {
                        "isMarket": True,
                        "slippage": 1
                    }
                }
            }
        ]
    }

    print(f">>> payload: \n{payload}")

    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()  # Check if request was successful
        print(">>> RESPONSE : ", response.json())  # Print the response data
    except requests.exceptions.RequestException as e:
        print(f">>> Error: {e}")


# Call the submitOrders function
submit_orders()

