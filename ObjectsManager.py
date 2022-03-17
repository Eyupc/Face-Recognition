from Database.DatabaseManager import DatabaseManager
from Recognition.TrainerManager import TrainerManager
from Recognition.users.UserManager import UserManager


class ObjectsManager:
    __databaseManager = DatabaseManager
    __userManager = UserManager
    __trainerManager = TrainerManager
    def __init__(self):
        self.loadAll()

    def loadAll(self):
        ObjectsManager.__databaseManager = DatabaseManager()
        ObjectsManager.__userManager = UserManager()
        ObjectsManager.__trainerManager = TrainerManager()

    @staticmethod
    def getDatabaseManager():
        return ObjectsManager.__databaseManager

    @staticmethod
    def getUserManager():
        return ObjectsManager.__userManager

    @staticmethod
    def getTrainerManager():
        return ObjectsManager.__trainerManager

    @staticmethod
    def getInstance():
        return
