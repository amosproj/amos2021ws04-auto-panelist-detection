import json
import time
from cv2 import cv2 # for autocompletion
import matplotlib.pyplot as plt
import numpy as np
import os

from insightface.app import FaceAnalysis
from deepface import DeepFace
from retinaface import RetinaFace

db_path = './database'

#face detection using opencv CascadeClassifier
class detector_faces_cv2():
    def __init__(self):
        opencv_home = cv2.__file__
        folders = opencv_home.split(os.path.sep)[0:-1]
        path = folders[0]
        for folder in folders[1:]:
            path = path + "/" + folder
        face_detector_path = path + "/data/haarcascade_frontalface_default.xml"
        print("[INFO] haar cascade configuration found here: ", face_detector_path)
        if os.path.isfile(face_detector_path) != True:
            raise ValueError("Confirm that opencv is installed on your environment! Expected path ", face_detector_path,
                             " violated.")
        self.haar_detector = cv2.CascadeClassifier(face_detector_path)
    def detect(self, img):
        self.faces_img = []
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.haar_detector.detectMultiScale(gray, 1.3, 5)
        for face in faces:
            x, y, w, h = face
            detected_face = img[int(y):int(y + h), int(x):int(x + w)]
            self.faces_img.append(detected_face)
    def get_faces_img(self):
        return self.faces_img
    def get_num_faces(self):
        return len(self.faces_img)


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

def facial_emotion_recognition_deepface(faces):
    start_time = time.time()
    emotions = []
    for face in faces:
        emotion = DeepFace.analyze(face, actions=['emotion'], detector_backend='skip')
        emotions.append(emotion)
    print("facial_emotion_recognition by deepface took", time.time() - start_time, "seconds to run")
    return emotions

# Age and gender estimation using caffe model from Rothe-IJCV-2018.
class age_gender_estimator:
    def __init__(self):
        print("[INFO] loading age/gender models...")
        # Download link for caffe models: https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/
        self.age_model = cv2.dnn.readNetFromCaffe("models/age.prototxt", "models/dex_chalearn_iccv2015.caffemodel")
        self.gender_model = cv2.dnn.readNetFromCaffe("models/gender.prototxt", "models/gender.caffemodel")
        self.output_indexes = np.array([i for i in range(0, 101)])
        print("[INFO] model loaded")
    def classifyAgeGender(self, faces_img):
        self.genders = []
        self.ages = []
        start = time.time()
        for face_img in faces_img:
            # x, y, w, h = face
            # detected_face = img[int(y):int(y + h), int(x):int(x + w)]
            # self.faces_img.append(detected_face)
            # age model is a regular vgg and it expects (224, 224, 3) shape input
            face_img = cv2.resize(face_img, (224, 224))
            img_blob = cv2.dnn.blobFromImage(face_img)  # caffe model expects (1, 3, 224, 224) shape input
            # ---------------------------
            self.age_model.setInput(img_blob)
            age_dist = self.age_model.forward()[0]
            apparent_predictions = round(np.sum(age_dist * self.output_indexes), 2)
            self.ages.append(apparent_predictions)
            # print("Apparent age: ", apparent_predictions)
            # ---------------------------
            self.gender_model.setInput(img_blob)
            gender_class = self.gender_model.forward()[0]
            gender = 'Woman ' if np.argmax(gender_class) == 0 else 'Man'
            self.genders.append(gender)
            # plt.imshow(detected_face[:, :, ::-1]); plt.axis('off')
            # plt.show()
        end = time.time()
        print(f'[INFO] Age / Gender recognition for {len(faces_img)} faces will require {end - start} seconds')
    def get_ages_genders(self):
        return self.ages, self.genders

