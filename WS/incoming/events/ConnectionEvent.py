from WS.WebSocketManager import WebSocketManager
from WS.incoming.IncomingMessage import IncomingMessage


class ConnectionEvent(IncomingMessage):
    def __init__(self,websocket, header, data):
        super().__init__(websocket,header, data)
        self.header = header
        self.data = data
        self.websocket = websocket

    async def execute(self):
        WebSocketManager.addClient(self.data['id'],self.websocket)




