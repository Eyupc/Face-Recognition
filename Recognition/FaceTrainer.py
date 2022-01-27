import base64
import io

import cv2
import json as JSON

from PIL import Image

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
        for img in image_:
            image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face_locations = detector.detectMultiScale(image)
            for faces in face_locations:
                x, y, w, h = faces
                face = image[y:y+h,x:x+w]
                self.encodedData = base64.b64encode(cv2.imencode('.jpg',face)[1]).decode("utf-8")
                self.trainingdata.append(self.encodedData)
        self.__addUser()
                #imgdata = base64.b64decode(self.encodedData)
                #imageJPG = Image.open(io.BytesIO(imgdata))
                #imageJPG.show()

    def __addUser(self):
        ObjectsManager.getUserManager().addUser(self.name,self.lastname,self.age,self.trainingdata)

