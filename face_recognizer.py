import os
import numpy as np
import cv2
import face_detector

def recognize_face(img):
    print(">> RECOGNIZING FACES...")
    # dau vao la 1 anh cv2 (output cua face_detector), dau ra la 1 name
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    path = './data'
    for f in os.listdir(path):
        name_path = os.path.join(path, f).replace('\\','/')
        print(name_path)
        recognizer.read(name_path + '/trainer.yml')
        id_, confidence = recognizer.predict(img)
        if confidence > 51:
            return f
        else:
            return None