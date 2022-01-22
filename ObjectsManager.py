from Database.DatabaseManager import DatabaseManager
from Recognition.users.UserManager import UserManager


class ObjectsManager:
    __databaseManager = DatabaseManager
    __userManager = UserManager
    def __init__(self):
       ObjectsManager.__databaseManager = DatabaseManager()
       ObjectsManager.__userManager = UserManager()


    @staticmethod
    def getDatabaseManager():
        return ObjectsManager.__databaseManager
    @staticmethod
    def getUserManager():
        return ObjectsManager.__userManager
