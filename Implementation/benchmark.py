from detection import detection
import image.draw as draw

import json
import time
import pandas as pd
import cv2
import os


class Benchmark:

    def __init__(self):
        detection.set_test_env()

    def run_benchmark_detection(self):
        detection_methods = ['Retina_Face']
        data_detection = {'Path': [], 'Method': [], 'Detection_Time': [], 'Faces_Truth': [], 'Faces_Static': [],
                          'Faces_Detected': [], 'Detection_Correct': [], 'Bounding_Boxes': []}
        f_detection = open('./test images/detection.json')
        detection_data = json.load(f_detection)
        f_detection.close()
        for img in detection_data:
            for method in detection_methods:
                st = time.time()
                bb_img = cv2.imread('./test images/' + img['path'])
                if method == 'Retina_Face':
                    number, faces, facial_areas = detection.detect_faces_deepface_RF(bb_img)
                else:
                    raise NotImplementedError
                t = time.time() - st
                detection_correct = (number == img['number'])
                for facial_area in facial_areas:
                    bb_img = draw.rectangle(bb_img, facial_area)
                filename = './benchmark/bounding_boxes/{}.jpg'.format(len(data_detection['Method']))
                if not os.path.isdir('./benchmark'):
                    os.mkdir('./benchmark')
                if not os.path.isdir('./benchmark/bounding_boxes'):
                    os.mkdir('./benchmark/bounding_boxes')
                cv2.imwrite(filename, bb_img)

                data_detection['Path'].append(img['path'])
                data_detection['Method'].append(method)
                data_detection['Detection_Time'].append(t)
                data_detection['Faces_Truth'].append(img['number'])
                data_detection['Faces_Static'].append(img['number_static'])
                data_detection['Faces_Detected'].append(number)
                data_detection['Detection_Correct'].append(detection_correct)
                data_detection['Bounding_Boxes'].append(filename)

        df = pd.DataFrame.from_dict(data_detection)
        df.to_csv('./benchmark/detection_benchmark.csv', index=False)

    def run_benchmark_recognition(self):
        recognition_methods = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]
        data_recognition = {'Path': [], 'Recognition_Method': [], 'Recognition_Time': [], 'Recognition_Correct': [],
                            'Gender_Time': [], 'Gender_Correct': [], 'Age_Time': [], 'Age_Correct': [],
                            'Emotion_Time': [], 'Emotion_Correct': []}
        f_recognition = open('./test images/recognition.json')
        recognition_data = json.load(f_recognition)
        f_recognition.close()
        for img in recognition_data:
            for method in recognition_methods:
                bb_img = cv2.imread('./test images/' + img['path'])
                _, faces, _ = detection.detect_faces_deepface_RF(bb_img)

                st_recognition = time.time()
                identity = detection.recognize_faces(faces[0])[0]
                t_recognition = time.time() - st_recognition
                recognition_correct = (identity == img['name'])

                st_gender = time.time()
                gender = detection.detect_gender(faces[0])
                t_gender = time.time() - st_gender
                if gender == "Woman":
                    gender = "f"
                elif gender == "Man":
                    gender = "m"
                gender_correct = (gender == img['gender'])

                st_age = time.time()
                age = detection.detect_age(faces[0])
                t_age = time.time() - st_age
                age_correct = (age in range(img['age'] - 10, img['age'] + 10))

                st_emotion = time.time()
                emotion = detection.detect_emotion(faces[0])
                t_emotion = time.time() - st_emotion
                emotion_correct = (emotion == img['emotion'])

                data_recognition['Path'].append(img['path'])
                data_recognition['Recognition_Method'].append(method)
                data_recognition['Recognition_Time'].append(t_recognition)
                data_recognition['Recognition_Correct'].append(recognition_correct)
                data_recognition['Gender_Time'].append(t_gender)
                data_recognition['Gender_Correct'].append(gender_correct)
                data_recognition['Age_Time'].append(t_age)
                data_recognition['Age_Correct'].append(age_correct)
                data_recognition['Emotion_Time'].append(t_emotion)
                data_recognition['Emotion_Correct'].append(emotion_correct)

        if not os.path.isdir('./benchmark'):
            os.mkdir('./benchmark')
        df = pd.DataFrame.from_dict(data_recognition)
        df.to_csv('./benchmark/recognition_benchmark.csv', index=False)


if __name__ == '__main__':
    bm = Benchmark()
    bm.run_benchmark_detection()
    bm.run_benchmark_recognition()





