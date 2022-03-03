import base64
import io

import cv2
import numpy as np
from PIL import Image


class TrainerManager:
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    def train(self):
        from ObjectsManager import ObjectsManager

        ids = []
        train_data = []

        for user in ObjectsManager.getUserManager().getUsers().values():

            for train in user.getTrainData():
                img = Image.open(io.BytesIO(base64.b64decode(train)))
                #img.show()
                train_data.append(np.array(img,'uint8'))
                ids.append(user.getId())

        try:
            self.recognizer.train(train_data, np.asarray(ids))
            self.recognizer.write("trainer.yml")
        except Exception:
            print("No users found")
