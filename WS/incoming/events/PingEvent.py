import asyncio
import json

from WS.WebSocketManager import WebSocketManager
from WS.incoming.IncomingMessage import IncomingMessage
import json

class PingEvent(IncomingMessage):
    def __init__(self, websocket, header, data):
        super().__init__(websocket, header, data)
        self.websocket = websocket
        self.header = header
        self.data = data

    async def execute(self):
        data = {
            "header":"PingEvent",
            "data": [{
                "id": WebSocketManager.getClient(self.websocket),
                "message":"Ping!"
            }]
        }
        await WebSocketManager.sendMessage(websocket=self.websocket,message=str(json.dumps(data)))

