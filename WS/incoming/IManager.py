from WS.incoming.events.SetPageEvent import SetPageEvent
from WS.incoming.events.AddUserEvent import AddUserEvent
from WS.incoming.events.ConnectionClosedEvent import ConnectionClosedEvent
from WS.incoming.events.ConnectionEvent import ConnectionEvent
from WS.incoming.events.PingEvent import PingEvent
from WS.incoming.events.DeleteUserEvent import DeleteUserEvent


class IncomingManager:
    def __init__(self):
        self.events = {}
        self.registerEvents()

    def registerEvents(self):
        self.events["ConnectionEvent"] = ConnectionEvent
        self.events["ConnectionClosedEvent"] = ConnectionClosedEvent
        self.events["PingEvent"] = PingEvent
        self.events["AddUserEvent"] = AddUserEvent
        self.events["DeleteUserEvent"] = DeleteUserEvent
        self.events["SetPageEvent"] = SetPageEvent
    def getEvent(self,event):
        return self.events[event]
