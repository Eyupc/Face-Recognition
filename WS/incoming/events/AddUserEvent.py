import json

from Recognition.FaceTrainer import FaceTrainer
from WS.WebSocketManager import WebSocketManager
from WS.incoming.IncomingMessage import IncomingMessage


class AddUserEvent(IncomingMessage):
    def __init__(self, websocket, header, data):
        IncomingMessage.__init__(self, websocket, header, data)

        self.header = header
        self.data = data
        self.websocket = websocket

    def execute(self):  # Voorbeeld hoe classe wordt opgeroepen, en de execute functie wordt opgeroepen.
        ft = FaceTrainer(self.data["name"], self.data["lastname"], self.data["age"], self.data["images"])
        faces = ft.trainFace()
        data = {
            "header": "AddUserEvent",
            "data": [{
                "id": WebSocketManager.getId(self.websocket),
                "faces_count": str(faces)
            }]
        }
        WebSocketManager.sendMessage(websocket=self.websocket, message=json.dumps(data))
