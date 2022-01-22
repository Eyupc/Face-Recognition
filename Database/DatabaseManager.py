import pymongo.database

from Database.DatabaseService import DatabaseService


class DatabaseManager:

    def __init__(self):
        self.__databaseService = DatabaseService("localhost",27017,"face-recognition")

    def getDatabaseService(self):
        return self.__databaseService

