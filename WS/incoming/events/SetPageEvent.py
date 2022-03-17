import asyncio
import json

from Recognition.FaceTrainer import FaceTrainer
from WS.WebSocketManager import WebSocketManager
from WS.incoming.IncomingMessage import IncomingMessage


class SetPageEvent(IncomingMessage):
    def __init__(self,websocket, header, data):
        super().__init__(websocket,header, data)
        self.header = header
        self.data = data
        self.websocket = websocket

    def execute(self):
       from ObjectsManager import ObjectsManager
       WebSocketManager.setPage(self.websocket,self.data["page"])




