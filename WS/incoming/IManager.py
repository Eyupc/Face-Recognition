from WS.incoming.events.ConnectionClosedEvent import ConnectionClosedEvent
from WS.incoming.events.ConnectionEvent import ConnectionEvent
from WS.incoming.events.PingEvent import PingEvent


class IncomingManager:
    def __init__(self):
        self.events = {}
        self.registerEvents()

    def registerEvents(self):
        self.events["ConnectionEvent"] = ConnectionEvent
        self.events["ConnectionClosedEvent"] = ConnectionClosedEvent
        self.events["PingEvent"] = PingEvent

    def getEvent(self,event):
        return self.events[event]
