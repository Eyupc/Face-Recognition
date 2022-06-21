import base64
import io
import json
import json as JSON
import time

import face_recognition
import ObjectsManager
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
            self.__users[id] = User(id, name, lastname, age, train_data)
        print("\n [INFO] Users from the database are registered!")

    def getUsers(self):
        return self.__users

    def getUser(self, id):
        return self.__users.get(id)

    def removeUser(self, id):
        from ObjectsManager import ObjectsManager
        # self.collection.delete_one({'id':id})
        if self.__users[id]:
            del self.__users[id]
            try:
                while True:
                    index = ObjectsManager.getTrainerManager().ids.index(id)
                    ObjectsManager.getTrainerManager().ids.remove(id)
                    ObjectsManager.getTrainerManager().encodings.pop(index)
                    # print(ObjectsManager.getTrainerManager().ids)
            except ValueError as e:
                return True
        else:
            return False

    def addUser(self, name, lastname, age, train_data):
        from ObjectsManager import ObjectsManager
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
        self.__users[userId] = User(userId, name, lastname, age, train_data)

        ObjectsManager.getMain().pause()
        time.sleep(1)
        self.__train(train_data, userId)

    def __train(self, train_data, userId):
        from ObjectsManager import ObjectsManager
        for train in train_data:
            try:
                f_l = face_recognition.load_image_file(io.BytesIO(base64.b64decode(train)))
                f_e = face_recognition.face_encodings(f_l)
                if len(f_e) >= 1:
                    ObjectsManager.getTrainerManager().ids.append(userId)
                    ObjectsManager.getTrainerManager().encodings.append(f_e[0])
            except Exception as e:
                print(str(e))
        ObjectsManager.getMain().resume()
