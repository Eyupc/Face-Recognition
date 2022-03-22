import asyncio
import base64
import threading

import cv2
import cv2.data
import time
import atexit

from WS.WebSocketManager import WebSocketManager


class Main:
    def __init__(self):
        from WS.WebSocketServer import WebSocketServer
        from ObjectsManager import ObjectsManager
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        self.obj = ObjectsManager
        self.obj.getTrainerManager().train()

        self.WebSocketServer = WebSocketServer()
        self.WebSocketServer.start()
        try:
            self.recognizer.read('trainer.yml')
        except Exception:
            print("[INFO] Trainer.yml is empty!")

        self.cam = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        self.cam.set(3, 640)
        self.cam.set(4, 480)
        self.minW = 0.2 * self.cam.get(3)
        self.minH = 0.2 * self.cam.get(4)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.startTime()

        self.loop = True

    def startTime(self):
        collection = self.obj.getDatabaseManager().getDatabaseService().getDatabase()['stats']
        collection.update_one({}, {'$set': {'start_time': time.time()}})

    def stop(self):
        collection = self.obj.getDatabaseManager().getDatabaseService().getDatabase()['stats']
        collection.update_one({}, {'$set': {'start_time': 0}})

        print("[INFO] Closing the program..")
        self.WebSocketServer.stop()
        self.loop = False
        self.cam.release()
        raise SystemExit()

    def updateReader(self):
        self.recognizer = None
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer.yml')

    def run(self):
        while self.loop:
            try:
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
                try:
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        if (len(self.obj.getUserManager().getUsers()) > 0):
                            id, confidence = -1, 200
                            try:
                                id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
                            except Exception as e:
                                print("[ERROR] " + str(e))

                            # print(id)
                            # print(confidence)
                            if confidence <= 90:
                                # print("id: " + str(id))
                                userInfo = self.obj.getUserManager().getUser(id)
                                user = userInfo.getName() + " " + userInfo.getLastname() + " " + str(userInfo.getAge())
                                confidence = "  {0}%".format(round(100 - confidence))
                            else:
                                user = "Unknown"
                                confidence = "  {0}%".format(round(100 - confidence))

                            (ww, hh), _ = cv2.getTextSize(str(user), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                            img = cv2.rectangle(img, (x, y), (x + ww, y - hh - 5), (0, 0, 255), -1)
                            img = cv2.putText(img, str(user), (x, y - 5),
                                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

                            # cv2.putText(img, str(user), (x + 5, y - 5), self.font, 1, (255, 255, 255), 2)
                            # cv2.putText(img, str(confidence), (x + 5, y + h - 5), self.font, 1, (255, 255, 0), 1)
                except Exception as e:
                    print("[INFO/ERROR] Updating Trainer.yml...\r\n Reason: " + str(e))
                    pass

                k = cv2.waitKey(10) & 0xff
                if k == 27:
                    raise KeyboardInterrupt

                cv2.imshow('video', img)

                base64_str = str(base64.b64encode(cv2.imencode('.jpg', img)[1]).decode("utf-8"))
                data = {
                    "header": "StreamEvent",
                    "data": [{
                        "message": base64_str
                    }]
                }
                self.WebSocketServer.ioloop.add_callback(WebSocketManager.sendBroadcast, data, "StreamPage")
            except KeyboardInterrupt as e:
                self.stop()
            except Exception as e:
                print("[ERROR]: " + str(e))


if __name__ == "__main__":
    from ObjectsManager import ObjectsManager

    obj = ObjectsManager()
    obj.getMain().run()
