import base64
import os

import cv2
import numpy as np
from PIL import Image

from Recognition.FaceTrainer import FaceTrainer

# obj = ObjectsManager()

imagePaths = [os.path.join('./images/', f) for f in os.listdir('./images/')]
faceSamples = []
ids = []
for imagePath in imagePaths:
    PIL_img = Image.open(imagePath)
    img_numpy = np.array(PIL_img, 'uint8')
    faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(
        img_numpy,
        scaleFactor=1.2,
        minNeighbors=5,
    )
    for (x, y, w, h) in faces:
        face = img_numpy[y:y + h, x:x + w]
        faceSamples.append(base64.b64encode(cv2.imencode('.jpg', face)[1]).decode("ascii"))
        # imgdata = base64.b64decode((base64.b64encode(cv2.imencode('.jpg',face)[1]).decode("utf-8")))
        # imageJPG = Image.open(io.BytesIO(imgdata))
        # imageJPG.show()

ft = FaceTrainer("Eyup", "Cakir", 22)
# print(len(faceSamples))
ft.trainFace(faceSamples)
