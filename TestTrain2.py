import base64
import io
import os

import cv2
import numpy as np
from PIL import Image

from ObjectsManager import ObjectsManager
from Recognition.FaceTrainer import detector, FaceTrainer

obj = ObjectsManager()

imagePaths = [os.path.join('./images/',f) for f in os.listdir('./images/')]
faceSamples=[]
ids = []
for imagePath in imagePaths:
    PIL_img = Image.open(imagePath).convert('L')
    img_numpy = np.array(PIL_img,'uint8')
    faces = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml").detectMultiScale(img_numpy)
    for (x,y,w,h) in faces:
        face = img_numpy[y:y+h,x:x+w]
        imen = cv2.imencode('.jpg',face)
        faceSamples.append(base64.b64encode(cv2.imencode('.jpg',face)[1]).decode("utf-8"))
        #imgdata = base64.b64decode((base64.b64encode(cv2.imencode('.jpg',face)[1]).decode("utf-8")))
        #imageJPG = Image.open(io.BytesIO(imgdata))
        #imageJPG.show()

ft = FaceTrainer("Kendall","Jenner",26)
print(len(faceSamples))
    #ft.trainFace(faceSamples)

