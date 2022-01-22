import base64
import io

import cv2
import face_recognition
import json as JSON

from PIL import Image

from Database.DatabaseService import DatabaseConnection
from Redis.RedisClient import RedisClient


class FaceTrainer:
    def __init__(self,name,lastname,age):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.age = age
        self.trainingdata = []
        self.encodedData = None

    def trainFace(self,image): #STILL TODO
        face_locations = face_recognition.face_locations(image)
        for faces in face_locations:
            for i in range(0,2):
                top, right, bottom, left = faces
                face = image[top:bottom,left:right]
                self.encodedData = base64.b64encode(cv2.imencode('.jpg',face)[1]).decode("utf-8")
                self.trainingdata.append(self.encodedData)

            self.insertToDatabase()
            #imgdata = base64.b64decode(FaceTrainer.test)
            #imageJPG = Image.open(io.BytesIO(imgdata))
            #imageJPG.show()

    def insertToDatabase(self):
        db = DatabaseConnection.getDatabase()['users_whitelisted']
        try:
            last_id = db.find().sort('_id', -1).limit(1)[0]['id'] + 1

        except IndexError:
            last_id = 1
        json = {
            'id': last_id,
            'name': self.name,
            'lastname': self.lastname,
            'age': self.age,
            'train_data': JSON.dumps(self.trainingdata)
        }
        db.insert_one(json)


