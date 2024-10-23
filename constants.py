# Constants for API
API_BASE_URL = "https://orderbook.filament.finance/sei"
EXCHANGE_URL = f"{API_BASE_URL}/filament/api/v1/exchange"

BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjB4NmI4OWRlYThiM2NhYjZhNWQzMTRlNWFjMzUxZjE5MjJlNmVlMzQzMiIsInN1YiI6IjB4NmI4OWRlYThiM2NhYjZhNWQzMTRlNWFjMzUxZjE5MjJlNmVlMzQzMiIsImlhdCI6MTcyOTAzNjgwMCwiZXhwIjoxNzI5Njg2NDU1fQ.tYO5UFjLHaUKa2s3TZtKffTT9Qvsv7EDNYQSdTCqGHM"  # Use your token
SIGNING_KEY = "0x7e0168eeabfa46d615112e2e689dfb62d73f9066699bb6a3ecef1242e12f438c"
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
}
INDEX_TOKEN = "BTC"  # BTC Index Token as example
ACOUNT = "0x6b89dEa8b3CAb6A5d314e5aC351f1922e6Ee3432"

NUM_ORDERS = 5

# WebSocket URLs
WEB_SOCKET_URL = (
    "https://orderbook.filament.finance/sei/api/order-book/orderbook-websocket"
)
