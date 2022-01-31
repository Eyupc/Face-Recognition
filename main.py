
import cv2
import cv2.data
import keyboard as keyboard
import numpy as np

from ObjectsManager import ObjectsManager
from Recognition.FaceTrainer import FaceTrainer
from Recognition.TrainerManager import TrainerManager
from mss import mss
class Main:
    def __init__(self):
        self.obj = ObjectsManager()
        self.trainer = TrainerManager()
        self.trainer.train()

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer.yml')

        self.cam = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        self.cam.set(3,640)
        self.cam.set(4,480)
        self.minW = 0.1 * self.cam.get(3)
        self.minH = 0.1 * self.cam.get(4)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        #self.bounding_box = {'top': 100, 'left': 1000, 'width': 900 , 'height': 540}
#
        #self.sct = mss()
    def run(self):
        while True:
            ret,img = self.cam.read()
            #img = np.array(self.sct.grab(self.bounding_box))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(self.minW), int(self.minH)),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if(len(self.obj.getUserManager().getUsers()) > 0):
                    id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
                    print(confidence)
                    if confidence <= 100:
                        userInfo = self.obj.getUserManager().getUser(id)
                        user = userInfo.getName() + " " + userInfo.getLastname() + " " + str(userInfo.getAge())
                        confidence = "  {0}%".format(round(100 - confidence))
                    else:
                        user = "Unknown"
                        confidence = "  {0}%".format(round(100 - confidence))

                    cv2.putText(img, str(user), (x + 5, y - 5), self.font, 1, (255, 255, 255), 2)
                    cv2.putText(img, str(confidence), (x + 5, y + h - 5), self.font, 1, (255, 255, 0), 1)

            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break

            cv2.imshow('video',img)


main = Main()
main.run()

#TODO FOTOS EXPERIMENTEREN
