from retinaface import RetinaFace
from deepface.detectors import RetinaFaceWrapper 
from deepface import DeepFace
from .anti_spoof_predict import AntiSpoofPredict
from .utility import parse_model_name
from .generate_patches import CropImage
from os.path import dirname as up

import numpy as np
import os


class detection():
    def __init__(self) -> None:
        # Creating face detection model
        self.face_detector = RetinaFace.build_model()

        # Panelist database 
        self.db_path = './../database'

        # Emotion Age Gender detection models (used by DeepFace.analyze() function). Pls use with detected faces (detector_backend ="skip")
        self.models_age = {"age": DeepFace.build_model('Age')}
        self.models_gender = {"gender":DeepFace.build_model('Gender') }
        self.models_emotion = {"emotion":DeepFace.build_model('Emotion') }

        # Create antispoof model
        self.model_test = AntiSpoofPredict(0)


    # Changing database path
    def set_env(self):
        self.db_path = './database'


    # Takes image and returns number of detected faces, corresponding images of aligned faces (based64 encoded), and facial areas
    def detect_faces_deepface_RF(self, img):
        resp = RetinaFaceWrapper.detect_face(self.face_detector,img,align=True)
        faces=[]
        facial_areas=[]

        # Prepare results in lists + switch facial area format from deepface to retinaface
        for face, facial_area in resp:
            faces.append(face)
            x,y,w,h = facial_area
            facial_areas.append([x,y,x+w,y+h]) 

        return len(faces),faces,facial_areas        


    # Same function as above without facial areas
    def detect_faces_deepface(self, img):
        faces = RetinaFace.extract_faces(img_path=img, align=True)
        num_people = len(faces)
        return num_people, faces


    # Takes array of detected faces and returns the recognized identity for each face
    # Facenet512 or VGG-Face produce best results
    def recognize_faces(self, faces, model='VGG-Face'):
        identities = []
        metrics = ["cosine", "euclidean", "euclidean_l2"] # euclidean_l2 works best for us. Lower score = more similarity.
        models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
        #TODO handle exceptions if no faces or no images in database

        # Finds the most similar identities for each face
        # detector_backend="skip": we already pass encoded faces 
        dfs = DeepFace.find(img_path = faces, db_path = self.db_path, model_name = model,detector_backend = 'skip', distance_metric = metrics[2], )
           
        if not isinstance(dfs,list):
            dfs = [dfs]

        # Get most similar identity for each face
        for df in dfs:
            cosine = df[model + '_euclidean_l2']
            if len(cosine) > 0:
                max_idx = np.argmin(cosine)
                identity_path = df['identity'][max_idx]
                identities.append(os.path.split(os.path.dirname(identity_path))[-1])
            else:
                identities.append('Unknown')

        return identities

    # For each face call corresponding age, gender, and emotion detection functions 
    # Returns genders, ages, and emotions as arrays 
    def analyze_faces(self, faces):
        genders = []
        ages = []
        emotions = []
        for face in faces:
            genders.append(self.detect_gender(face))
            ages.append(self.detect_age(face))
            emotions.append(self.detect_emotion(face))
        return genders, ages, emotions


    def attentiveness(self, faces):
        raise NotImplementedError

    # Detects if face is real #TODO 
    def liveness_detector(self, frame, bboxes):
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
            new_bbox = self.get_new_bbox(r,radius)
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
                prediction += self.model_test.predict(img, os.path.join(model_dir, model_name))

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
    def get_new_bbox(self, r, radius):
        cx = r
        cy = r
        bbox = [None] * 4
        # bbox like x,y,w,h
        bbox[0] = cx-radius
        bbox[1] = cy-radius
        bbox[2] = radius * 2
        bbox[3] = radius * 2
        return bbox

    # The following three functions take one face and return detected emotion/gender/age
    def detect_emotion(self, img):
        result = DeepFace.analyze(img,actions=["emotion"],models=self.models_emotion,detector_backend ="skip")
        return result["dominant_emotion"]

    def detect_gender(self, img):
        result = DeepFace.analyze(img,actions=["gender"],models=self.models_gender,detector_backend ="skip")
        return result["gender"]

    def detect_age(self, img):
        result = DeepFace.analyze(img,actions=["age"],models=self.models_age,detector_backend ="skip")
        return result["age"]