import json

import ObjectsManager
from Database.DatabaseManager import DatabaseManager
from Recognition.users.User import User


class UserManager:

    def __init__(self):
        self.collection = ObjectsManager.DatabaseManager().getDatabaseService().getDatabase()['users_whitelisted']
        self.__users = {}
        self.__registerUsers()

    def __registerUsers(self):
        cursor = self.collection.find({})
        for records in cursor:
            id = int(records['id'])
            name = records['name']
            lastname = records['lastname']
            age = records['age']
            train_data = json.loads(str(records['train_data']))
            self.__users[id] = User(id,name,lastname,age,train_data)
        print("\n [INFO] Users from the database are registered!")

    def getUsers(self):
        return self.__users

    def getUser(self,id):
        return self.__users.get(id)

    def removeUser(self,id):
        del self.__users[id]

    def addUser(self, User):
        self.__users[User.getId()] = User



