import base64
import io
import threading
import cv2
import face_recognition
from ObjectsManager import ObjectsManager
from Recognition.FaceTrainerr import FaceTrainer

obj = ObjectsManager()
cam = cv2.VideoCapture(0)

while True:
    ret,img = cam.read()
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        faceT = FaceTrainer('Ahmo', 'Zer', 25)
        faceT.trainFace(img)
        break
    cv2.imshow('video',img)
