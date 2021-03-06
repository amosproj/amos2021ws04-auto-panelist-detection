import unittest
import time
import json
import numpy as np
from detection.detection import Detection


class TestOnImages(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load labels from JSON files that contain labels for all images to be tested
        f_detection = open('./test images/detection.json')
        cls.detection_data = json.load(f_detection)
        f_detection.close()

        f_recognition = open('./test images/recognition.json')
        cls.recognition_data = json.load(f_recognition)
        f_recognition.close()

        cls.detection = Detection()
        cls.detection.set_env()

    # test detection
    def test_detection(self):
        durations = []
        for img in self.detection_data:
            st = time.time()
            number, _ = self.detection.detect_faces_deepface('./test images/' + img['path'])
            self.assertEqual(number, img['number'])
            t = time.time() - st
            durations.append(t)
        print('Average detection time: {} s'.format(np.mean(durations)))

    # test recognition
    def test_recognition(self):
        durations = []
        for img in self.recognition_data:
            _, faces = self.detection.detect_faces_deepface('./test images/' + img['path'])
            st = time.time()
            identity = self.detection.recognize_faces(faces[0])[0]
            self.assertEqual(identity, img['name'])
            t = time.time() - st
            durations.append(t)
        print('Average recognition time: {} s'.format(np.mean(durations)))

    # test age detection
    def test_age_detection(self):
        durations = []
        for img in self.recognition_data:
            _, faces = self.detection.detect_faces_deepface('./test images/' + img['path'])
            st = time.time()
            age = self.detection.detect_age(faces[0])
            self.assertAlmostEqual(age, img['age'], None, None, 10)
            t = time.time() - st
            durations.append(t)
        print('Average age detection time: {} s'.format(np.mean(durations)))

    # test emotion detection
    def test_emotion_detection(self):
        # ! emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        durations = []
        for img in self.recognition_data:
            _, faces = self.detection.detect_faces_deepface('./test images/' + img['path'])
            st = time.time()
            emotion = self.detection.detect_emotion(faces[0])
            self.assertEqual(emotion, img['emotion'])
            t = time.time() - st
            durations.append(t)
        print('Average emotion detection time: {} s'.format(np.mean(durations)))

    # test gender detection
    def test_gender_detection(self):
        durations = []
        for img in self.recognition_data:
            _, faces = self.detection.detect_faces_deepface('./test images/' + img['path'])
            st = time.time()
            gender = self.detection.detect_gender(faces[0])

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
