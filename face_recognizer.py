import os

def recognize_face(img):
    print(">> RECOGNIZING FACES...")
    # dau vao la 1 anh cv2 (output cua face_detector), dau ra la 1 name
    data_folder = "data/"
    labels = [folder for folder in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, folder))]

    labels = ['test']

    return labels[0]