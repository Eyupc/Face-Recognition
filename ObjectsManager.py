from Database.DatabaseManager import DatabaseManager
from Recognition.TrainerManager import TrainerManager
from Recognition.users.UserManager import UserManager
from WS.incoming.IManager import IncomingManager


class ObjectsManager:
    __databaseManager = DatabaseManager
    __userManager = UserManager
    __incomingManager = IncomingManager
    __trainerManager = TrainerManager
    def __init__(self):
        pass

    def loadAll(self):
        ObjectsManager.__databaseManager = DatabaseManager()
        ObjectsManager.__userManager = UserManager()
        ObjectsManager.__incomingManager = IncomingManager()
        ObjectsManager.__trainerManager = TrainerManager()

    @staticmethod
    def getDatabaseManager():
        return ObjectsManager.__databaseManager

    @staticmethod
    def getUserManager():
        return ObjectsManager.__userManager
    @staticmethod
    def getIncomingerManager():
        return ObjectsManager.__incomingManager

    @staticmethod
    def getTrainerManager():
        return ObjectsManager.__trainerManager

    @staticmethod
    def getInstance():
        return
