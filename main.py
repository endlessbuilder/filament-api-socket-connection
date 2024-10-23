import time

from filament_api import cancel_order, get_order_book, submit_limit_order
from filament_stomp_socket import connect_to_websocket


# Main Function to Manage WebSocket and REST Calls
def main():
    # Connect and subscribe to the WebSocket feed
    connect_to_websocket()

    # Wait for WebSocket to establish
    time.sleep(3)

    # Fetch Order Book using REST API (public)
    print("\n>>> get order book\n")
    get_order_book()

    # Submit Batch Orders (private)
    print("\n>>> submit order\n")
    order_id = submit_limit_order()

    # Cancel all orders (private)
    time.sleep(10)  # Wait for some time before cancelling
    print("\n>>> cancel order\n")
    cancel_order(order_id)

    # Keep script running to maintain WebSocket connection
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
