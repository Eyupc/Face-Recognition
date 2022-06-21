import base64
import io

import face_recognition


class TrainerManager:
    ids = []
    encodings = []

    def __init__(self):
        pass

    def train(self):
        from ObjectsManager import ObjectsManager
        for user in ObjectsManager.getUserManager().getUsers().values():
            for train in user.getTrainData():
                # img = Image.open(io.BytesIO(base64.b64decode(train)))
                # img.show()
                # decoded = ur.urlopen("data:image/png;base64," + train)
                # image = face_recognition.load_image_file(decoded)

                arr = face_recognition.face_encodings(
                    face_recognition.load_image_file(io.BytesIO(base64.b64decode(train))))
                if len(arr) >= 1:
                    TrainerManager.encodings.append(arr[0])
                    TrainerManager.ids.append(user.getId())

        print("[INFO] Encoding of images is done!")
        try:
            pass
        except Exception:
            print("No users found")

    def addId(self):
        pass

    def addTrain(self):
        pass
