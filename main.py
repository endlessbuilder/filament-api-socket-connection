import time

from filament_stomp_socket import connect_to_websocket


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
