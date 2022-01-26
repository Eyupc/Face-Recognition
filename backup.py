
import cv2
import cv2.data
import keyboard

from ObjectsManager import ObjectsManager
from Recognition.FaceTrainer import FaceTrainer
from Recognition.TrainerManager import TrainerManager


obj = ObjectsManager()

cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)
ct = 0

trainer = TrainerManager()

data = []
faceT = FaceTrainer('Kendall', 'Jenner', 26)

while True:
    ret,img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if(keyboard.is_pressed('a')):
            if ct != 10:
                ct +=1
                data.append(img)
            else:
                ct+=1
                faceT.trainFace(data)
                trainer.train()
    print(ct)
    if ct == 11:
        break

    k = cv2.waitKey(10) & 0xff
    cv2.imshow('video',img)
