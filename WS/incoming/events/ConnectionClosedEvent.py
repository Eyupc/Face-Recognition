from WS.WebSocketManager import WebSocketManager
from WS.incoming.IncomingMessage import IncomingMessage


class ConnectionClosedEvent(IncomingMessage):
    def __init__(self,websocket, header, data):
        super().__init__(websocket,header, data)
        self.header = header
        self.data = data
        self.websocket = websocket

    async def execute(self):
        WebSocketManager.removeClient(self.data['id'])




