import json

import ObjectsManager
from Database.DatabaseManager import DatabaseManager
from Recognition.users.User import User


class UserManager:

    def __init__(self):
        self.__users = []
        self.__registerUsers()

    def __registerUsers(self):
        collection = ObjectsManager.DatabaseManager().getDatabaseService().getDatabase()['users_whitelisted']
        cursor = collection.find({})
        for records in cursor:
            id = str(records['id'])
            name = records['name']
            lastname = records['lastname']
            age = records['age']
            train_data = json.loads(str(records['train_data']))
            self.__users.append(User(id,name,lastname,age,train_data))
        print("\n [INFO] Users from the database are registered!")

    def getUsers(self):
        return self.__users

    def getUser(self,id):
        for user in self.__users:
            if int(user.getId()) == id:
                return user


