import base64
import io

import cv2
import numpy as np
from PIL import Image

from ObjectsManager import ObjectsManager


class TrainerManager:
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.data = None

    def train(self):
        ids = ObjectsManager.getUserManager().getUsers().keys()
        train_data = []
        for user in ObjectsManager.getUserManager().getUsers().values():
            print(user.getTrainData()[0])
            img = Image.open(io.BytesIO(base64.b64decode(user.getTrainData()[0])))
            train_data.append(np.array(img,'uint8'))

        self.recognizer.train(train_data, np.array(ids))
        self.recognizer.write(self.data) #TODO

    def getData(self):
        return self.data
