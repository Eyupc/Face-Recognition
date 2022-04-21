import asyncio
import base64
import json
import threading
import time

import cv2
import cv2.data
import dlib
import face_recognition
import numpy as np

from WS.WebSocketManager import WebSocketManager
from WSClient.WebSocketClient import WebSocketClient
from utils.DateManager import DateManager
from utils.NumpyEncoder import NumpyEncoder


class Main:
    def __init__(self):
        from WS.WebSocketServer import WebSocketServer
        from ObjectsManager import ObjectsManager
        self.recognizer = cv2.face.LBPHFaceRecognizer_create(threshold=0.0)

        self.obj = ObjectsManager
        self.obj.getTrainerManager().train()  # Train faces -> get data from db

        self.WebSocketServer = WebSocketServer()  # Face Recognition Websocket Server
        self.WebSocketServer.start()

        # self.WebSocketClient = WebSocketClient()  # ESP Websocket Client
        # self.WebSocketClient.start()

        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cam.set(3, 640)
        self.cam.set(4, 480)
        self.minW = 0.2 * self.cam.get(3)
        self.minH = 0.2 * self.cam.get(4)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.updateStats()

        self.loop = True
        self.loop_time = time.time()
        self.last_update_date = ""

        self.isRecognized = False
        self.First_Recognize_time = 0

        self.process_this_frame = True
        self.lastStream = None

        self.close = False

    def updateStats(self):
        collection = self.obj.getDatabaseManager().getDatabaseService().getDatabase()['stats']
        collection.update_one({}, {'$set': {'start_time': time.time()}})

        update_date = collection.find_one({},{'update_date'})
        self.last_update_date = update_date["update_date"]

    def increaseRecognizedAmount(self):
        collection = self.obj.getDatabaseManager().getDatabaseService().getDatabase()['stats']
        print(DateManager.getTodayDayName())
        collection.update_one({},{'$inc': {('recognized_amount.'+DateManager.getTodayDayName()): 1}})

    def stop(self):
        collection = self.obj.getDatabaseManager().getDatabaseService().getDatabase()['stats']
        collection.update_one({}, {'$set': {'start_time': 0}})

        print("[INFO] Closing the program..")
        self.WebSocketServer.stop()
        self.loop = False
        self.cam.release()


       # f = open("trainer.yml","w")
       # f.write(json.dumps({'encodings': self.obj.getTrainerManager().encodings, 'ids': self.obj.getTrainerManager().ids},
       #            cls=NumpyEncoder))
#
       # f.close()



        raise SystemExit()

    def pause(self):
        print("[INFO] Updating users...")
        self.close = True
        self.cam.release()

    def resume(self):
        print("[INFO]: Updated users!")
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cam.set(3, 640)
        self.cam.set(4, 480)
        self.loop = True
        self.close = False
        self.process_this_frame = True


    def run(self):
        while True:
            while self.loop:
                try:
                    ret, img = self.cam.read()
                    small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
                    rgb_small_frame = small_frame[:, :, ::-1]
                    if self.process_this_frame:
                        try:
                            countFaces = 0
                            user = "UnKnown"
                            face_locations = face_recognition.face_locations(rgb_small_frame, model="mtcnn")
                            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                            for face_encoding in face_encodings:
                                countFaces += 1
                                if len(self.obj.getUserManager().getUsers()) > 0:
                                    id, confidence = -1, 200
                                    matches = face_recognition.compare_faces(self.obj.getTrainerManager().encodings,
                                                                             face_encoding, tolerance=0.4)
                                    # name = "Unknown"

                                    if True in matches:
                                        first_match_index = matches.index(True)
                                        id = self.obj.getTrainerManager().ids[first_match_index]
                                    # face_distances = face_recognition.face_distance(self.obj.getTrainerManager().encodings, face_encodings[0])
                                    # best_match_index = np.argmin(face_distances)

                                    # if matches[best_match_index]:
                                    #   id = self.obj.getTrainerManager().ids[best_match_index]
                                    # id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])

                                    # print(id)
                                    # print(str(id) + " " + str(100 - confidence))

                                    print(id)
                                    if id > -1:
                                        if not self.isRecognized:
                                            self.isRecognized = True
                                            self.First_Recognize_time = time.time()
                                        # print(confidence)
                                        # print("id: " + str(id))
                                        userInfo = self.obj.getUserManager().getUser(id)
                                        user = userInfo.getName() + " " + userInfo.getLastname() + " " + str(
                                            userInfo.getAge())
                                    else:
                                        if self.isRecognized:
                                            self.isRecognized = False
                                            self.First_Recognize_time = 0

                                        user = "Unknown"

                            for (top, right, bottom, left) in face_locations:
                                top *= 4
                                right *= 4
                                bottom *= 4
                                left *= 4

                                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
                                cv2.rectangle(img, (left, top - 35), (right, top), (0, 0, 255), cv2.FILLED)
                                font = cv2.FONT_HERSHEY_DUPLEX
                                font = cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(img, user, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)
                            self.lastStream = img
                            if self.isRecognized:
                                if countFaces == 0:
                                    self.isRecognized = False
                                    self.First_Recognize_time = 0

                                elif time.time() - self.First_Recognize_time >= 3:
                                    data = {
                                        "header": "OpenDoorEvent",
                                        "data": [{
                                            "open": True
                                        }]
                                    }

                                    # self.WebSocketClient.sendMessage(json.dumps(data))
                                    self.increaseRecognizedAmount()

                                    self.isRecognized = False
                                    self.First_Recognize_time = 0
                        except Exception as e:
                            print("[INFO/ERROR]\r\n Reason: " + str(e))
                            pass

                    self.process_this_frame = not self.process_this_frame

                    k = cv2.waitKey(10) & 0xff

                    if (self.close == True) | (str(ret) == "False"):
                        # print("IN GEGAAN")
                        self.loop = False
                        cv2.destroyAllWindows()
                        break

                    if k == 27:
                        raise KeyboardInterrupt
                    cv2.imshow('stream', img)

                    base64_str = str(base64.b64encode(cv2.imencode('.jpg', self.lastStream)[1]).decode("utf-8"))
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
                    if self.close == True:
                        self.loop = False
                        cv2.destroyAllWindows()
                        break


if __name__ == "__main__":
    from ObjectsManager import ObjectsManager

    obj = ObjectsManager()
    obj.getMain().run()
