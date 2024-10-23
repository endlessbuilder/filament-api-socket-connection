import time
from websocket import create_connection
import webstompy

from constants import INDEX_TOKEN, WEB_SOCKET_URL
from utils import get_socket_server


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
