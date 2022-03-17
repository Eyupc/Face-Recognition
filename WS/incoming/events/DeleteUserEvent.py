from Recognition.TrainerManager import TrainerManager
from WS.WebSocketManager import WebSocketManager
from WS.incoming.IncomingMessage import IncomingMessage


class DeleteUserEvent(IncomingMessage):
    def __init__(self,websocket, header, data):
        super().__init__(websocket,header, data)
        self.header = header
        self.data = data
        self.websocket = websocket

    def execute(self):
        from ObjectsManager import ObjectsManager
        result = ObjectsManager.getUserManager().removeUser(self.data["user_id"])
        TrainerManager().train()
        ObjectsManager.getMain().updateReader()
        data = {
            "header":"DeleteUserEvent",
            "data":[{
                "id":WebSocketManager.getId(self.websocket),
                "status": str(result)
            }]
        }

       # WebSocketManager.sendMessage(websocket=self.websocket,message=json.dumps(data))




