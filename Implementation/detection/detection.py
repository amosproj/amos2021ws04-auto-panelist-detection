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


def detect_faces_deepface(img_path):
    faces = RetinaFace.extract_faces(img_path=img_path, align=True)
    num_people = len(faces)
    return num_people, faces


def recognize_faces(faces):
    identities = []
    for face in faces:
        #plt.imshow(face)
        #plt.show()
        recognized = DeepFace.find(face, db_path=db_path, detector_backend='skip')
        cosine = recognized['VGG-Face_cosine']
        if len(cosine) > 0:
            max_idx = np.argmax(cosine)
            identity_path = recognized['identity'][max_idx]
            identities.append(os.path.split(os.path.dirname(identity_path))[-1])
        else:
            identities.append('Unknown')
    return identities


def analyze_faces(faces):
    genders = []
    ages = []
    emotions = []
    for face in faces:
        # plt.imshow(face)
        # plt.show()
        analyzed = DeepFace.analyze(face, detector_backend='skip')
        genders.append(analyzed['gender'])
        ages.append(analyzed['age'])
        emotions.append(analyzed['dominant_emotion'])
    return genders, ages, emotions


def attentiveness(faces):
    raise NotImplementedError


def detect_faces_RF(img_path):
    faces = RetinaFace.detect_faces(img_path) 
    return faces

def get_facial_areas_RF(faces):
    facial_areas=[]
    for face in faces:
        facial_area = faces[face]["facial_area"]
        facial_areas.append(facial_area)
    return facial_areas
