class WebSocketManager:
    __clients = {}
    def __init__(self):
        pass
    @staticmethod
    def addClient(id,websocket):
        WebSocketManager.__clients[id] = websocket

    @staticmethod
    def removeClient(id):
        del WebSocketManager.__clients[id]

    @staticmethod
    def removeClientByWS(websocket):
        for k,v in WebSocketManager.__clients.items():
            print(k)
            print(v)
            if v==websocket:
                del WebSocketManager.__clients[k]
                return

    @staticmethod
    def getClient(id):
        return WebSocketManager.__clients[id]
    @staticmethod
    def getClients():
        return WebSocketManager.__clients