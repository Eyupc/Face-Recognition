from WS.incoming.events.ConnectionClosedEvent import ConnectionClosedEvent
from WS.incoming.events.ConnectionEvent import ConnectionEvent


class IncomingManager:
    def __init__(self):
        self.events = {}
        self.registerEvents()

    def registerEvents(self):
        self.events["ConnectionEvent"] = ConnectionEvent
        self.events["ConnectionClosedEvent"] = ConnectionClosedEvent

    def getEvent(self,event):
        return self.events[event]
