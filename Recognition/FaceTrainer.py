import base64
import io
import threading

import cv2
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create(threshold=5.0)
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


class FaceTrainer:
    def __init__(self,name,lastname,age,images):
        self.name = name
        self.lastname = lastname
        self.age = age
        self.images = images
        self.trainingdata = []
        self.ids = []
        self.encodedData = None

    def trainFace(self): #images in base64 format
        count = 0
        image_ = []
        for img_from_client in self.images:
            imgdata = base64.b64decode(img_from_client)
            imgJPG  = Image.open(io.BytesIO(imgdata))
            image_.append(np.array(imgJPG,'uint8'))

        for img in image_:
            try:
                image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            except Exception:
                image = img
            face_locations = detector.detectMultiScale(image,
                                                       scaleFactor=1.2,
                                                       minNeighbors=5,
                                                       minSize=(30, 30)
                                                       )
            for faces in face_locations:
                count +=1
                x, y, w, h = faces
                face = image[y:y+h,x:x+w]
                self.encodedData = base64.b64encode(cv2.imencode('.jpg',cv2.resize(face,(200,200)))[1]).decode("utf-8")
                self.trainingdata.append(self.encodedData)
        if count > 0:
            self.__addUser()
        return count

    def __addUser(self):
        from ObjectsManager import ObjectsManager
        ObjectsManager.getUserManager().addUser(self.name,self.lastname,self.age,self.trainingdata)
