class WebSocketManager:
    __clients = {}

    def __init__(self):
        pass

    @staticmethod
    def addClient(websocket, id):
        WebSocketManager.__clients[websocket] = id

    @staticmethod
    def removeClient(websocket):
        del WebSocketManager.__clients[websocket]

    @staticmethod
    def getClient(id):
        clients = WebSocketManager.__clients
        return list(clients.keys())[list(clients.values()).index(id)]

    @staticmethod
    def getId(websocket):
        return WebSocketManager.__clients[websocket]

    @staticmethod
    def getClients():
        return WebSocketManager.__clients.keys()

    @staticmethod
    def sendBroadcast(message):
        clients = WebSocketManager.__clients.keys()
        try:
            for client in clients:
                if client.ws_connection.stream.socket:
                    client.write_message(message, binary=True)
        except Exception as e:
            print("Error: " + str(e))

    @staticmethod
    def sendMessage(websocket, message: str):
        if websocket.ws_connection.stream.socket:
            websocket.write_message(message, binary=True)
