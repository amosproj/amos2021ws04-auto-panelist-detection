
import json
import time
from insightface.app import FaceAnalysis
from retinaface import RetinaFace
from deepface.detectors import RetinaFaceWrapper 
from deepface import DeepFace
from cv2 import cv2 # for autocompletion
import matplotlib.pyplot as plt
import numpy as np
import os

face_detector = RetinaFace.build_model()
db_path = './../database'



def set_test_env():
    global db_path
    db_path = './database'


def detect_faces_deepface_RF(img):
    # detects faces, returns aligned faces (based64 encoded) and facial areas
    resp = RetinaFaceWrapper.detect_face(face_detector,img,align=True)
    faces=[]
    facial_areas=[]

    # prepare results in lists + switch facial area format from deepface to retinaface
    for face, facial_area in resp:
        faces.append(face)
        x,y,w,h = facial_area
        facial_areas.append([x,y,x+w,y+h])  
    return len(faces),faces,facial_areas        

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
    return num_people, faces


def recognize_faces(faces):
    identities = []
    metrics = ["cosine", "euclidean", "euclidean_l2"] # for computing similarity. Lower score = more similarity.
    #TODO handle exceptions if no faces or no images in database

    # Finds the most similar identities for each face # Afaik ArcFace+euclidean_l2 showed best results # skip detection: we already pass encoded faces
    dfs = DeepFace.find(img_path = faces, db_path = db_path, model_name = 'ArcFace',detector_backend = 'skip', distance_metric = metrics[2])
    if not isinstance(dfs,list):
        dfs = [dfs]

    # Get most similar identity for each face
    for df in dfs:
        #plt.imshow(face)
        #plt.show()
        cosine = df['ArcFace_euclidean_l2']
        
        if len(cosine) > 0:
            max_idx = np.argmin(cosine)
            identity_path = df['identity'][max_idx]
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

def facial_emotion_recognition_deepface():
    start_time = time.time()
    facial_emotion = DeepFace.analyze(img_path='../test images/Ben/ben-collins-6CFmQSQlTz4-unsplash.jpg', actions=['emotion'])
    print(facial_emotion) #type dict
    print("facial_emotion_recognition by deepface took", time.time() - start_time, "to run")



