import asyncio
import json

from Recognition.FaceTrainer import FaceTrainer
from WS.WebSocketManager import WebSocketManager
from WS.incoming.IncomingMessage import IncomingMessage


class AddUserEvent(IncomingMessage):
    def __init__(self,websocket, header, data):
        super().__init__(websocket,header, data)
        self.header = header
        self.data = data
        self.websocket = websocket

    def execute(self):
        ft = FaceTrainer(self.data["name"],self.data["lastname"],self.data["age"])
        faces = ft.trainFace(self.data["images"])
        print(len(self.data["images"]))
        data = {
            "header":"AddUserEvent",
            "data":[{
                "id":WebSocketManager.getId(self.websocket),
                "faces_count":str(faces)
            }]
        }
        #print(faces)
        WebSocketManager.sendMessage(websocket=self.websocket,message=json.dumps(data))



