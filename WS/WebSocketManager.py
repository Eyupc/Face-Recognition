import asyncio


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
            if v==websocket:
                del WebSocketManager.__clients[k]
                return

    @staticmethod
    def getClient(id):
        return WebSocketManager.__clients[id]
    @staticmethod
    def getClients():
        return WebSocketManager.__clients

    @staticmethod
    async def sendBroadcast(message):
        clients = WebSocketManager.__clients.values()
        res = None
        try:
            if(len(clients) == 1):
                res = await list(clients)[0].send(message)
                return res
            elif(len(clients) > 1):
                for ws in clients:
                    res = ws.send(message)
                return res
        except Exception as e:
            print(e)
