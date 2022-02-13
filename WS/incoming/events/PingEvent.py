import json

from WS.WebSocketManager import WebSocketManager
from WS.incoming.IncomingMessage import IncomingMessage


class PingEvent(IncomingMessage):
    def __init__(self, websocket, header, data):
        super().__init__(websocket, header, data)
        self.websocket = websocket
        self.header = header
        self.data = data

    def execute(self):
        data = {
            "header":"PingEvent",
            "data": [{
                "id": WebSocketManager.getId(self.websocket),
                "message":"Ping!"
            }]
        }

        WebSocketManager.sendMessage(websocket=self.websocket,message=str(json.dumps(data)))
