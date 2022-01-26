
import cv2
import cv2.data
import keyboard as keyboard

from ObjectsManager import ObjectsManager
from Recognition.FaceTrainer import FaceTrainer
from Recognition.TrainerManager import TrainerManager


obj = ObjectsManager()
trainer = TrainerManager()
trainer.train()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)
font = cv2.FONT_HERSHEY_SIMPLEX

ct = 0
while True:
    ret,img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    user = "None"
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
       #f(keyboard.is_pressed('a')): #TODO
       #   if ct != 10:
       #       ct +=1
       #       faceT = FaceTrainer('messi', 'lionel', 36)
       #       faceT.trainFace(img)
       #   else:
       #       trainer.train()
       #       recognizer.read("trainer.yml")

        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        print(confidence)
        if (confidence < 60):
            userInfo = obj.getUserManager().getUser(id)
            user = userInfo.getName() + " " + userInfo.getLastname() + " " + str(userInfo.getAge())
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            user = "Unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, str(user), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

    k = cv2.waitKey(10) & 0xff
    if k == 27:
        faceT = FaceTrainer('Ahmo', 'Zer', 25)
        faceT.trainFace(img)
        break
    cv2.imshow('video',img)
