from cv2 import cv2 # for autocompletion
import matplotlib.pyplot as plt
import numpy as np
import os

from insightface.app import FaceAnalysis

from deepface import DeepFace
from retinaface import RetinaFace

db_path = './database'


def detect_faces(img, show_img):
    app = FaceAnalysis()
    app.prepare(ctx_id=0, det_size=(640, 640))
    faces = app.get(img)
    num_people = len(faces)
    if show_img:
        res = app.draw_on(img, faces)
        cv2.imshow('orig', img)
        cv2.imshow('res', res)
        cv2.waitKey()
    return num_people


def detect_faces_deepface(img):
    faces = RetinaFace.extract_faces(img_path=img, align=True)
    num_people = len(faces)
    print('Number of people detected: {}'.format(num_people))
    for face in faces:
        plt.imshow(face)
        plt.show()
        recognized = DeepFace.find(face, db_path=db_path, detector_backend='skip')
        analyzed = DeepFace.analyze(face, detector_backend='skip')
        cosine = recognized['VGG-Face_cosine']
        if len(cosine) > 0:
            max_idx = np.argmax(cosine)
            identity_path = recognized['identity'][max_idx]
            identity = os.path.split(os.path.dirname(identity_path))[-1]
        else:
            identity = 'Unknown'
        gender = analyzed['gender']
        age = analyzed['age']
        emotion = analyzed['dominant_emotion']
        print('{}, {}, {} years old. Dominant emotion: {}'.format(identity, gender, age, emotion))
        return num_people


#detect_faces_deepface("/home/janis/Dropbox/data/faces/test/test1.jpg")



def detect_faces_RF(img_path):
    faces = RetinaFace.detect_faces(img_path) 
    return faces

def get_facial_areas_RF(faces):
    facial_areas=[]
    for face in faces:
        facial_area = faces[face]["facial_area"]
        facial_areas.append(facial_area)
    return facial_areas