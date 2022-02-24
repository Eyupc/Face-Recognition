from Recognition.FaceTrainer import FaceTrainer
from WS.incoming.IncomingMessage import IncomingMessage


class AddUserEvent(IncomingMessage):
    def __init__(self,websocket, header, data):
        super().__init__(websocket,header, data)
        self.header = header
        self.data = data
        self.websocket = websocket

    def execute(self):
        print(self.data)
        ft = FaceTrainer(self.data["name"],self.data["lastname"],self.data["age"])
        faces = ft.trainFace(self.data["images"])
        self.websocket.write_message(str(faces))




