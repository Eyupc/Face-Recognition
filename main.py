import asyncio
import base64
import threading
from threading import Thread

import cv2
import cv2.data
import keyboard as keyboard
import numpy as np
import websockets

from ObjectsManager import ObjectsManager
from Recognition.FaceTrainer import FaceTrainer
from Recognition.TrainerManager import TrainerManager
from mss import mss

from WS.WebSocketManager import WebSocketManager
from WS.WebSocketServer import WebSocketServer


class Main:
    def __init__(self):
        self.obj = ObjectsManager()
        self.trainer = TrainerManager()
        self.trainer.train()

        self.WebSocketServer = WebSocketServer("localhost", 6969)
        self.thread = Thread(target=self.WebSocketServer.run)
        self.thread.start()

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer.yml')

        self.cam = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        self.cam.set(3, 640)
        self.cam.set(4, 480)
        self.minW = 0.1 * self.cam.get(3)
        self.minH = 0.1 * self.cam.get(4)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        # self.bounding_box = {'top': 100, 'left': 1000, 'width': 900 , 'height': 540}

        # self.sct = mss()

    async def run(self):
        while True:
            ret, img = self.cam.read()
            # img = np.array(self.sct.grab(self.bounding_box))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml').detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(self.minW), int(self.minH)),
            )

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if (len(self.obj.getUserManager().getUsers()) > 0):
                    id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
                    # print(confidence)
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

            base64_str = str(base64.b64encode(cv2.imencode('.jpg', img)[1]).decode("utf-8"))
            await self.sendStream(base64_str)
            cv2.imshow('video', img)

    async def sendStream(self, img):#TODO
        #print(threading.enumerate())
        clients = WebSocketManager.getClients().values()
        for v in clients:
            try:
                await v.send(img)
            except Exception as e:
                print("Error: " + str(e))

main = Main()
asyncio.get_event_loop().run_until_complete(main.run())
# TODO FOTOS EXPERIMENTERE
