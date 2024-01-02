import os

def train():
    print(">> TRAINING NEW FILES...")
    data_folder = "data/"
    labels = [folder for folder in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, folder))]
    
    for user in labels:
        path = data_folder + user + "/"
        #   save/process j day
    
    # train -> save ra file train de import vao face_recognizer.py

