## REQUIREMENTS
Python script that can fulfil these basic functions:
1. Connect to websocket with authentication
2. Subscribe to example public and private streams using the websocket, e.g. open orders
3. Demonstrate output returned over the websocket
4. Demonstrate REST API public and private endpoint usage for example requests, such as get bid/ask (public), submit batch orders & cancel all orders (private)
5. Run a heartbeat to check the exchange connection is alive & handle reconnect if it dies

Summarise, it connects to their public and provate data streams so we can view their price feed lets use BTC as an example. 

The script can place batch limit orders and also cancel them via rest api, continually pings the WS to recivce a pong message.
It doesn't need to actually do anything specifically, if it can place a batch of 5 bids and 5 asks or even just 1 bit/ask and can cancel them that would be enough.

So, 
1. Data stream from the CEX
2. Batch order submission and cancelation via REST api