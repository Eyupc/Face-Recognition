import base64

import cv2
import json as JSON

from ObjectsManager import ObjectsManager
from Recognition.users.User import User
from Recognition.users.UserManager import UserManager

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


class FaceTrainer:
    def __init__(self,name,lastname,age):
        self.name = name
        self.lastname = lastname
        self.age = age
        self.trainingdata = []
        self.ids = []
        self.encodedData = None

    def trainFace(self,image_): #STILL TODO
        image = cv2.cvtColor(image_, cv2.COLOR_BGR2RGB)
        face_locations = detector.detectMultiScale(image)
        for faces in face_locations:
            x, y, w, h = faces
            face = image[y:y+h,x:x+w]
            self.encodedData = base64.b64encode(cv2.imencode('.jpg',face)[1]).decode("utf-8")
            self.trainingdata.append(self.encodedData)
            self.__insertToDatabase()
            self.__addUser()
            #imgdata = base64.b64decode(FaceTrainer.test)
            #imageJPG = Image.open(io.BytesIO(imgdata))
            #imageJPG.show()

    def __insertToDatabase(self):
        db = ObjectsManager.getDatabaseManager().getDatabaseService().getDatabase()['users_whitelisted']
        try:
            self.id = db.find().sort('_id', -1).limit(1)[0]['id'] + 1

        except IndexError:
            self.id = 1
        json = {
            'id': self.id,
            'name': self.name,
            'lastname': self.lastname,
            'age': self.age,
            'train_data': JSON.dumps(self.trainingdata)
        }
        db.insert_one(json)

    def __addUser(self):
        ObjectsManager.getUserManager().addUser(User(self.id,self.name,self.lastname,self.age,self.trainingdata))

