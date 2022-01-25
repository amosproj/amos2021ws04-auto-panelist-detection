import unittest
import time
import json
import numpy as np
from detection import detection


class TestOnImages(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        f_detection = open('./test images/detection.json')
        cls.detection_data = json.load(f_detection)
        f_detection.close()

        f_recognition = open('./test images/recognition.json')
        cls.recognition_data = json.load(f_recognition)
        f_recognition.close()

        detection.set_env()

    def test_detection(self):
        durations = []
        for img in self.detection_data:
            st = time.time()
            number, _ = detection.detect_faces_deepface('./test images/' + img['path'])
            self.assertEqual(number, img['number'])
            t = time.time() - st
            durations.append(t)
        print('Average detection time: {} s'.format(np.mean(durations)))

    def test_recognition(self):
        durations = []
        for img in self.recognition_data:
            _, faces = detection.detect_faces_deepface('./test images/' + img['path'])
            st = time.time()
            identity = detection.recognize_faces(faces[0])[0]
            self.assertEqual(identity, img['name'])
            t = time.time() - st
            durations.append(t)
        print('Average recognition time: {} s'.format(np.mean(durations)))

    def test_age_detection(self):
        durations = []
        for img in self.recognition_data:
            _, faces = detection.detect_faces_deepface('./test images/' + img['path'])
            st = time.time()
            age = detection.detect_age(faces[0])
            self.assertAlmostEqual(age, img['age'], None, None, 10)
            t = time.time() - st
            durations.append(t)
        print('Average age detection time: {} s'.format(np.mean(durations)))

    def test_emotion_detection(self):
        # ! emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        durations = []
        for img in self.recognition_data:
            _, faces = detection.detect_faces_deepface('./test images/' + img['path'])
            st = time.time()
            emotion = detection.detect_emotion(faces[0])
            self.assertEqual(emotion, img['emotion'])
            t = time.time() - st
            durations.append(t)
        print('Average emotion detection time: {} s'.format(np.mean(durations)))

    def test_gender_detection(self):
        durations = []
        for img in self.recognition_data:
            _, faces = detection.detect_faces_deepface('./test images/' + img['path'])
            st = time.time()
            gender = detection.detect_gender(faces[0])

            if gender == "Woman":
                gender = "f"
            elif gender == "Man":
                gender = "m"

            self.assertEqual(gender, img['gender'])
            t = time.time() - st
            durations.append(t)
        print('Average gender detection time: {} s'.format(np.mean(durations)))


if __name__ == '__main__':
    unittest.main()
