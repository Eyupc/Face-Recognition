
import cv2

from ObjectsManager import ObjectsManager
from Recognition.FaceTrainer import FaceTrainer
from Recognition.TrainerManager import TrainerManager

obj = ObjectsManager()
cam = cv2.VideoCapture(0)

trainer = TrainerManager()
trainer.train()
#print(trainer.getData())
exit(0)
while True:
    ret,img = cam.read()
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        faceT = FaceTrainer('Ahmo', 'Zer', 25)
        faceT.trainFace(img)
        break
    cv2.imshow('video',img)
