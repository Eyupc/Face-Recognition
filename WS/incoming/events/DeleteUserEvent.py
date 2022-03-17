import asyncio
import json

from Recognition.FaceTrainer import FaceTrainer
from WS.WebSocketManager import WebSocketManager
from WS.incoming.IncomingMessage import IncomingMessage


class DeleteUserEvent(IncomingMessage):
    def __init__(self,websocket, header, data):
        super().__init__(websocket,header, data)
        self.header = header
        self.data = data
        self.websocket = websocket

    def execute(self):
        #print(self.data)
        from ObjectsManager import ObjectsManager
        import main
        #print(ObjectsManager.getUserManager().getUsers())
        data = {
            "header":"DeleteUserEvent",
            "data":[{
                "id":WebSocketManager.getId(self.websocket),
                "status": "result"
            }]
        }
        WebSocketManager.sendMessage(websocket=self.websocket,message=json.dumps(data))




