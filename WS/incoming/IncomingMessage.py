from abc import ABC, abstractmethod

class IncomingMessage(ABC):

    def __init__(self,websocket,header,data):
        self.websocket = websocket
        self.header = header
        self.data = data

    @abstractmethod
    def execute(self):
        pass


