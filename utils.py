def get_socket_server(server_url):
    url = server_url + "/websocket"
    if url[:5] == "https":
        url = "wss" + url[5:]
    else:
        url = "ws" + url[4:]

    print(">>> web socket url : ", url)
    return url
