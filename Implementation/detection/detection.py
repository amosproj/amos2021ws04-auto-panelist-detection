from insightface.app import FaceAnalysis
from retinaface import RetinaFace
from deepface import DeepFace
from cv2 import cv2
from .anti_spoof_predict import AntiSpoofPredict
from .utility import parse_model_name
from .generate_patches import CropImage
from os.path import dirname as up



import matplotlib.pyplot as plt
import numpy as np
import json
import time
import os

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


def detect_faces_RF(img_path):
    faces = RetinaFace.detect_faces(img_path)
    return faces


def get_facial_areas_RF(faces):
    facial_areas = []
    for face in faces:
        facial_area = faces[face]["facial_area"]
        facial_areas.append(facial_area)
    return facial_areas


def facial_emotion_recognition_deepface():
    start_time = time.time()
    facial_emotion = DeepFace.analyze(img_path='../test images/Ben/ben-collins-6CFmQSQlTz4-unsplash.jpg',
                                      actions=['emotion'])
    print(facial_emotion)  # type dict
    print("facial_emotion_recognition by deepface took", time.time() - start_time, "to run")

model_test = AntiSpoofPredict(0)
def liveness_detector(frame, image_bbox):
    image_cropper = CropImage()
    dir = up(up(__file__))
    model_dir = os.path.join(dir, 'models/anti_spoof_models')
    # model_dir = '../models/anti_spoof_models'
    # image_bbox = model_test.get_bbox(frame)
    # if image_bbox[0] == 0 and image_bbox[1] == 0 and image_bbox[2] == 1 and image_bbox[3] == 1:
    #     return False
    prediction = np.zeros((1, 3))
    # test_speed = 0
    # sum the prediction from single model's result
    for model_name in os.listdir(model_dir):
        h_input, w_input, model_type, scale = parse_model_name(model_name)
        param = {
            "org_img": frame,
            "bbox": image_bbox,
            "scale": scale,
            "out_w": w_input,
            "out_h": h_input,
            "crop": True,
        }
        if scale is None:
            param["crop"] = False
        img = image_cropper.crop(**param)
        prediction += model_test.predict(img, os.path.join(model_dir, model_name))

    # label: face is true or fake
    label = np.argmax(prediction)
    # value: the score of prediction
    value = prediction[0][label]
    if label == 1 and value > 0.7:
        return True
    else:
        return False

