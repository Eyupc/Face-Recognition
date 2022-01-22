import cv2
import face_recognition
from ObjectsManager import ObjectsManager

objManager = ObjectsManager()

def main():
    cam = cv2.VideoCapture(0)
    while True:
        ret, img = cam.read()
        face_locations = face_recognition.face_locations(img)
        # face_encodings = face_recognition.face_encodings(img,face_locations)
        # for faces in face_encodings:
        #    results = face_recognition.compare_faces([ff],faces)
        #    if(results[0]):
        ##print('oki')
        for faces in face_locations:
            top, right, bottom, left = faces
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            break
        cv2.imshow("video", img)
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            #faceT = FaceTrainer('Eyup', 'Master', 20)
            #faceT.trainFace(img)
            break

    print("\n [INFO] Exiting Program.")
    cam.release()
    cv2.destroyAllWindows()

main()
