import cv2
import numpy as np
from skimage.feature import local_binary_pattern

MIN_SIZE = 75
MARGIN = 30

def extract_face(PATH:str = None, img = None):
    if PATH != None:
        img = cv2.imread(PATH)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    face_box = face_classifier.detectMultiScale(gray_img, scaleFactor=1.3, minNeighbors=5)
    
    if len(face_box) == 0:
        # No face detected
        if False: # Check for too dark image
            return (-1, 'Area too dark', [])
        elif False: # Check for too bright image
            return (-2, 'Area too bright', [])
        else:
            return (0, 'No face detected', [])
    elif len(face_box) > 1:
        # Too many faces detected
        return (-3, 'Too many faces detected', face_box)
    else:
        # Crop face
        fx, fy, fw, fh = face_box[0]
        if fw < MIN_SIZE or fh < MIN_SIZE:
            # Face too small
            return (-4, 'Move closer', face_box)
        elif fx < MARGIN or fy < MARGIN or fx+fw > img.shape[1]-MARGIN or fy+fh > img.shape[0]-MARGIN:
            # Face too close to the edge
            return (-5, 'Move to center', face_box)
        gray_img_face = gray_img[fy:fy+fh, fx:fx+fw]
        
        # EYES DETECTION - FACIAL ALIGNMENT
        eye_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")
        eye_box = eye_classifier.detectMultiScale(gray_img_face, scaleFactor=1.1, minNeighbors=4)
        
        if len(eye_box) >= 2:
            if eye_box[0][0] < eye_box[1][0]:
                left_eye = eye_box[0]
                right_eye = eye_box[1]
            else:
                left_eye = eye_box[1]
                right_eye = eye_box[0]
            center_left_eye = (int(left_eye[0] + left_eye[2] / 2), int(left_eye[1] + left_eye[3] / 2))
            center_right_eye = (int(right_eye[0] + right_eye[2] / 2), int(right_eye[1] + right_eye[3] / 2))
            if center_left_eye[1] > center_right_eye[1]:
                delta_M_right = np.linalg.norm(np.array((center_right_eye[0], center_left_eye[1])) - np.array(center_right_eye))
                delta_M_left = np.linalg.norm(np.array((center_right_eye[0], center_left_eye[1])) - np.array(center_left_eye))
                angle = - np.arctan(delta_M_right / delta_M_left)
            else:
                delta_M_right = np.linalg.norm(np.array((center_left_eye[0], center_right_eye[1])) - np.array(center_right_eye))
                delta_M_left = np.linalg.norm(np.array((center_left_eye[0], center_right_eye[1])) - np.array(center_left_eye))
                angle = np.arctan(delta_M_left / delta_M_right)
            angle = (angle * 180.) / np.pi
            # Rotate image
            (h, w) = gray_img.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            gray_img = cv2.warpAffine(gray_img, M, (w, h))
        else:
            # No eyes or side view detected
            return (-6, 'Please look directly', face_box)
        
        return (1, gray_img[fy-MARGIN:fy+fh+MARGIN, fx-MARGIN:fx+fw+MARGIN], face_box)
        # cv2.imwrite('output.jpg', img[fy:fy+fh, fx:fx+fw])
        
        # gray_img_pre = gray_img[fy-MARGIN:fy+fh+MARGIN, fx-MARGIN:fx+fw+MARGIN]
        # lbp_img = local_binary_pattern(gray_img_pre, 8, 1, method='default')
        # return (1, lbp_img, face_box)

