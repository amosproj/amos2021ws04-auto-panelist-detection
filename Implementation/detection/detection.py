from insightface.app import FaceAnalysis
from retinaface import RetinaFace
from deepface import DeepFace
from cv2 import cv2

import matplotlib.pyplot as plt
import numpy as np
import json
import time
import os


###
import face_recognition

from facenet_pytorch import MTCNN
import torch
import dlib

mtcnn = None  # facenet model will be loaded here if needed.

frontal_face_detect= None # dlib model will be loaded here if needed.
cnn_face_detect = None # dlib model will be loaded here if needed.

face_cascade = None # cv2 cascades classifier will be loaded here if needed.
###




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
    return num_people, faces


def recognize_faces(faces):
    identities = []
    for face in faces:
        # plt.imshow(face)
        # plt.show()
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


def facial_emotion_recognition_deepface():
    start_time = time.time()
    facial_emotion = DeepFace.analyze(img_path='../test images/Ben/ben-collins-6CFmQSQlTz4-unsplash.jpg',
                                      actions=['emotion'])
    print(facial_emotion)  # type dict
    print("facial_emotion_recognition by deepface took", time.time() - start_time, "to run")



##RetinaFace  
def detect_faces_RF(img_path):
    faces = RetinaFace.detect_faces(img_path) 
    return faces

def get_facial_areas_RF(faces):
    facial_areas=[]
    for face in faces:
        facial_area = faces[face]["facial_area"]
        facial_areas.append(facial_area)
    return facial_areas



##Facenet
def setup_facenet():
    global mtcnn
    if mtcnn == None:
        #device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        device = torch.device('cpu')

        mtcnn = MTCNN(keep_all=True, device=device)

def get_facial_areas_FACENET(frame):
    global mtcnn
    if mtcnn==None:
        print("setting up facenet")
        setup_facenet()
    facial_areas, conf = mtcnn.detect(frame)

    return facial_areas



##dlib_frontal
def setup_dlib_frontal():
    global frontal_face_detect
    if frontal_face_detect == None:
        frontal_face_detect = dlib.get_frontal_face_detector()

def detect_faces_DLIB_FRONTAL(img_path):
    global frontal_face_detect
    if frontal_face_detect == None:
        setup_dlib_frontal()
    img = cv2.imread(img_path)
    #img = cv2.resize(img, (600, 400))
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = frontal_face_detect(img, 1)
    return faces

def get_facial_areas_DLIB_FRONTAL(faces):
    facial_areas=[]
    for face in faces:
        x1 = face.left()
        y1 = face.bottom()
        x2 = face.right()
        y2 = face.top()
        facial_area= [x1,y1,x2,y2]
        facial_areas.append(facial_area)
    return facial_areas

##dlib_cnn
def setup_dlib_cnn():
    global cnn_face_detect
    if cnn_face_detect == None:
        cnn_face_detect = dlib.cnn_face_detection_model_v1("models/mmod_human_face_detector.dat")


def detect_faces_DLIB_CNN(img_path):
    global cnn_face_detect
    if cnn_face_detect == None:
        setup_dlib_cnn()
    img = cv2.imread(img_path)
    #img = cv2.resize(img, (600, 400))
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = cnn_face_detect(img, 1)
    return faces

def get_facial_areas_DLIB_CNN(faces):
    facial_areas=[]
    for face in faces:
        x1 = face.rect.left()
        y1 = face.rect.bottom()
        x2 = face.rect.right()
        y2 = face.rect.top()
        facial_area= [x1,y1,x2,y2]
        facial_areas.append(facial_area)
    return facial_areas



##cv2_cascades
def setup_cv2_cascades():
    global face_cascade
    if face_cascade == None:
        face_cascade = cv2.CascadeClassifier('models/cv2_data/haarcascade_frontalface_alt2.xml')

def detect_faces_CV2_CASCADES(img_path):
    global face_cascade
    if face_cascade == None:
        setup_cv2_cascades()

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)
    return faces

def get_facial_areas_CV2_CASCADES(faces):
    facial_areas=[]
    for face in faces:
        x, y, w, h = face
        x, y, w, h = int(x), int(y), int(w), int(h)
        facial_area= [x,y,x+w,y+h]
        facial_areas.append(facial_area)
    return facial_areas




def face_recognition_(img_path,img_path2): #  face_recognition is only compatible (accurate) with dlib detection
    known_image = face_recognition.load_image_file(img_path)
    unknown_image = face_recognition.load_image_file(img_path2)

    known_facial_areas  = get_facial_areas_DLIB_FRONTAL(detect_faces_DLIB_FRONTAL(img_path))
    unknown_facial_areas= get_facial_areas_DLIB_FRONTAL(detect_faces_DLIB_FRONTAL(img_path2))

    known_encoding = face_recognition.face_encodings(known_image,known_facial_areas,num_jitters=5)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image,unknown_facial_areas,num_jitters=5)[0]

    results = face_recognition.face_distance([known_encoding], unknown_encoding)
    #print(results)
    return results < 0.6
