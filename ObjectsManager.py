from Database.DatabaseManager import DatabaseManager
from Recognition.TrainerManager import TrainerManager
from Recognition.users.UserManager import UserManager
from main import Main


class ObjectsManager:
    __databaseManager = DatabaseManager
    __userManager = UserManager
    __trainerManager = TrainerManager

    __Main = Main

    def __init__(self):
        self.loadAll()

    def loadAll(self):
        ObjectsManager.__databaseManager = DatabaseManager()
        ObjectsManager.__userManager = UserManager()
        ObjectsManager.__trainerManager = TrainerManager()
        ObjectsManager.__Main = Main()

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
    def getMain():
        return ObjectsManager.__Main

    @staticmethod
    def getInstance():
        return
