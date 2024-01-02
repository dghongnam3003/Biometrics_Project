import os
import cv2
import numpy as np
from PIL import Image
import face_detector
from skimage.feature import local_binary_pattern

def train(name):
    print(">> TRAINING NEW FILES...")
    # data_folder = "data/"
    path = './data/' + name + '/photo'
    # labels = [folder for folder in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, folder))]
    
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    # for user in labels:
    #     path = data_folder + user + "/"
    #     #   save/process j day
    
    # train -> save ra file train de import vao face_recognizer.py

    
    def getImagesAndLabels(path):
        """
        Load face images and corresponding labels from the given directory path.
    
        Parameters:
            path (str): Directory path containing face images.
    
        Returns:
            list: List of face samples.
            list: List of corresponding labels.
        """
        
        faceSamples = []
        ids = []
        
        for f in os.listdir(path):
            ids.append(int(f.replace('.jpg','')))
            img = cv2.imread(os.path.join(path, f).replace('\\','/'), cv2.IMREAD_GRAYSCALE)
            lbp_img = local_binary_pattern(img, 8, 1, method='default')
            faceSamples.append(lbp_img)
            
            # for (x, y, w, h) in faces:
            #     # Extract face region and append to the samples
            #     faceSamples.append(img_numpy[y:y+h, x:x+w])
            
        return faceSamples, ids
    
    faces, ids = getImagesAndLabels(path)
    
    recognizer.train(faces, np.array(ids))
    
    recognizer.write('./data/' + name + '/trainer.yml')
    
    print("\n[INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
    
    # print(faces)
    # print(ids)