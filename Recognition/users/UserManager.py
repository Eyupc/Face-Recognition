import json
import json as JSON

import ObjectsManager
from Recognition.users.User import User


class UserManager:

    def __init__(self):
        self.collection = ObjectsManager.DatabaseManager().getDatabaseService().getDatabase()['users_whitelisted']
        self.__users = {}
        self.__registerUsers()
        print("ok")

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
        #self.collection.delete_one({'id':id})
        if self.__users[id]:
            del self.__users[id]
            return True
        else:
            return False

    def addUser(self, name,lastname,age,train_data):
        db = self.collection
        try:
            userId = db.find().sort('_id', -1).limit(1)[0]['id'] + 1

        except IndexError:
            userId = 1
        json = {
            'id': userId,
            'name': name,
            'lastname': lastname,
            'age': age,
            'train_data': JSON.dumps(train_data)
        }
        db.insert_one(json)
        self.__users[userId] = User(userId,name,lastname,age,train_data)


