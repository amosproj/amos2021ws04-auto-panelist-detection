import json
import time
from insightface.app import FaceAnalysis
from retinaface import RetinaFace
from deepface.detectors import RetinaFaceWrapper 
from deepface import DeepFace
from .anti_spoof_predict import AntiSpoofPredict
from .utility import parse_model_name
from .generate_patches import CropImage
from os.path import dirname as up
import math




from cv2 import cv2 # for autocompletion
import matplotlib.pyplot as plt
import numpy as np
import os

face_detector = RetinaFace.build_model()
db_path = './../database'



def set_env():
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


def recognize_faces(faces, model='ArcFace'):
    identities = []
    metrics = ["cosine", "euclidean", "euclidean_l2"] # for computing similarity. Lower score = more similarity.
    models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
    #TODO handle exceptions if no faces or no images in database

    # Finds the most similar identities for each face # Afaik ArcFace+euclidean_l2 showed best results # skip detection: we already pass encoded faces
    dfs = DeepFace.find(img_path = faces, db_path = db_path, model_name = model,detector_backend = 'skip', distance_metric = metrics[1])
    if not isinstance(dfs,list):
        dfs = [dfs]

    # Get most similar identity for each face
    for df in dfs:
        #plt.imshow(face)
        #plt.show()
        cosine = df[model + '_euclidean']
        
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
        #analyzed = DeepFace.analyze(face, detector_backend='skip')
        #genders.append(analyzed['gender'])
        #ages.append(analyzed['age'])
        #emotions.append(analyzed['dominant_emotion'])

        genders.append(detect_gender(face))
        ages.append(detect_age(face))
        emotions.append(detect_emotion(face))
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

model_test = AntiSpoofPredict(0)
def liveness_detector(frame, bboxes):
    image_cropper = CropImage()
    dir = up(up(__file__))
    model_dir = os.path.join(dir, 'models/anti_spoof_models')
    # height, width = frame.shape[0], frame.shape[1]
    # aspect_ratio = width / height
    # if frame.shape[1] * frame.shape[0] >= 192 * 192:
    #     img = cv2.resize(frame,
    #                      (int(192 * math.sqrt(aspect_ratio)),
    #                       int(192 / math.sqrt(aspect_ratio))), interpolation=cv2.INTER_LINEAR)
    results = []
    for bbox in bboxes:
        #only for bbox like x1,y1,x2,y2
        #temp1 = frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        cx = (bbox[0]+bbox[2])//2
        cy = (bbox[3]+bbox[1])//2
        radius = max(w,h)//2
        h, w, _ = frame.shape
        if (cx+radius*4) >= w or (cy+radius*4) >= h or (cx-radius*4) <=0 or (cy-radius*4)<0:
            factor = min(w-cx, cx, h-cy, cy) / radius
            r = int(radius * factor)
        else:
            r = radius*4
        # thanks to https://stackoverflow.com/questions/47580887/adjust-size-and-position-of-bounding-boxes-while-keeping-it-somewhat-centered
        croped = frame[cy-r:cy+r, cx-r:cx+r]
        new_bbox = get_new_bbox(r,radius)
        #temp2 = croped[new_bbox[1]:new_bbox[1]+new_bbox[3], new_bbox[0]:new_bbox[0]+new_bbox[2]]
        prediction = np.zeros((1, 3))
        # test_speed = 0
        # sum the prediction from single model's result
        for model_name in os.listdir(model_dir):
            h_input, w_input, model_type, scale = parse_model_name(model_name)
            param = {
                "org_img": croped,
                "bbox": new_bbox,
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
            result = True
        else:
            result = False
        results.append(result)
    return results

#r: new expanded radius, radius: original face area radius
def get_new_bbox(r, radius):
    cx = r
    cy = r
    bbox = [None] * 4
    # bbox like x,y,w,h
    bbox[0] = cx-radius
    bbox[1] = cy-radius
    bbox[2] = radius * 2
    bbox[3] = radius * 2
    return bbox


# Emotion Age Gender detection models (separate) # deepface models + without model reload # use with detected faces (detector_backend ="skip")
models_age = {}
models_gender = {}
models_emotion = {}
models_age['age'] = DeepFace.build_model('Age')
models_gender['gender'] = DeepFace.build_model('Gender')
models_emotion['emotion'] = DeepFace.build_model('Emotion')
# This is necessary because of the DeepFace.analyze() function

def detect_emotion(img,model=models_emotion):
    result = DeepFace.analyze(img,actions=["emotion"],models=model,detector_backend ="skip")
    return result["dominant_emotion"]

def detect_gender(img,model=models_gender):
    result = DeepFace.analyze(img,actions=["gender"],models=model,detector_backend ="skip")
    return result["gender"]

def detect_age(img,model=models_age):
    result = DeepFace.analyze(img,actions=["age"],models=model,detector_backend ="skip")
    return result["age"]

# example usage:
# def main():
#     img_path = "test images/James.jpg"
#     img = cv2.imread(img_path)

#     num_detected, faces, facial_areas = detection.detect_faces_deepface_RF(img) 
#     print(len(faces))

#     print(detection.detect_age(faces[0]))
#     print(detection.detect_emotion(faces[0]))
#     print(detection.detect_gender(faces[0]))