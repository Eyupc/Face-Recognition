from Database.DatabaseManager import DatabaseManager
from Recognition.users.UserManager import UserManager
from WS.incoming.IManager import IncomingManager


class ObjectsManager:
    __databaseManager = DatabaseManager
    __userManager = UserManager
    __incomingManager = IncomingManager
    def __init__(self):
        ObjectsManager.__databaseManager = DatabaseManager()
        ObjectsManager.__userManager = UserManager()
        ObjectsManager.__incomingManager = IncomingManager()

    @staticmethod
    def getDatabaseManager():
        return ObjectsManager.__databaseManager

    @staticmethod
    def getUserManager():
        return ObjectsManager.__userManager
    @staticmethod
    def getIncomingerManager():
        return ObjectsManager.__incomingManager