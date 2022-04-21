import tornado
from tornado import iostream

class WebSocketManager:
    __clients = {}

    def __init__(self):
        pass

    @staticmethod
    def addClient(websocket, id,page):
        WebSocketManager.__clients[websocket] = {
            "id":id,
            "page":page
        }

    @staticmethod
    def setPage(websocket,page):
        WebSocketManager.__clients[websocket]["page"] = page

    @staticmethod
    def removeClient(websocket):
        del WebSocketManager.__clients[websocket]

    @staticmethod
    def getClient(id):
        clients = WebSocketManager.__clients
        return list(clients.keys())[list(clients.values()).index(id)]

    @staticmethod
    def getId(websocket):
        return WebSocketManager.__clients[websocket]["id"]

    @staticmethod
    def getClients():
        return WebSocketManager.__clients.keys()

    @staticmethod
    def sendBroadcast(message,page):
        clients = WebSocketManager.__clients.keys()
        try:
            for client in clients:
                if client.ws_connection.stream.socket:
                    if WebSocketManager.__clients[client]["page"] == page:
                        client.write_message(message, binary=True)
        except Exception as e:
            print("Error: " + str(e))

    @staticmethod
    def sendMessage(websocket, message: str):
        try:
            if websocket.ws_connection.stream.socket:
                websocket.write_message(message, binary=True)
        except tornado.iostream.StreamClosedError as e:
            pass


