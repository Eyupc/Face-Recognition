import websockets

from utils.TextConverter import TextConverter


class WebSocketManager:
    __clients = {}
    def __init__(self):
        pass
    @staticmethod
    def addClient(id,websocket):
        WebSocketManager.__clients[websocket] = id

    @staticmethod
    def removeClient(ws):
        del WebSocketManager.__clients[ws]

    @staticmethod
    def getClient(websocket):
        return WebSocketManager.__clients[websocket]
    @staticmethod
    def getClients():
        return WebSocketManager.__clients.keys()

    @staticmethod
    def sendBroadcast(message):
        try:
            websockets.broadcast(WebSocketManager.__clients.keys(),TextConverter.encodeString(message))
        except Exception as e:
            print("Error: " + str(e))

    @staticmethod
    async def sendMessage(websocket,message:str):
        await websocket.send(TextConverter.encodeString(message))

