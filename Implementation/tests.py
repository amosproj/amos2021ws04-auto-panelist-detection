import unittest
import time
import json
import numpy as np
from detection import detection


class TestOnImages(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        f = open('./test images/test_images.json')
        cls.test_data = json.load(f)
        cls.faces = []
        cls.ages = []
        cls.emotions = []
        cls.genders = []
        f.close()
        detection.set_test_env()

    def test_detection(self):
        durations = []
        for img in self.test_data:
            st = time.time()
            number, faces = detection.detect_faces_deepface('./test images/' + img['path'])
            self.faces.append(faces)
            self.assertEqual(number, img['number'])
            t = time.time() - st
            durations.append(t)
        print('Average detection time: {} s'.format(np.mean(durations)))

    def test_age_detection(self):
        durations = []
        for img in self.test_data:
            st = time.time()
            age = detection.detect_age('./test images/' + img['path'])
            self.ages.append(age)
            self.assertEqual(age, img['age'])
            t = time.time() - st
            durations.append(t)
        print('Average detection time: {} s'.format(np.mean(durations)))

    def test_emotion_detection(self):
        #! emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        durations = []
        for img in self.test_data:
            st = time.time()
            emotion = detection.detect_emotion('./test images/' + img['path'])
            self.emotions.append(emotion)
            self.assertEqual(emotion, img['emotion'])
            t = time.time() - st
            durations.append(t)
        print('Average detection time: {} s'.format(np.mean(durations)))

    def test_gender_detection(self):
        durations = []
        for img in self.test_data:
            st = time.time()
            gender = detection.detect_gender('./test images/' + img['path'])

            if gender == "Woman":
                gender = "f"
            elif gender== "Man":
                gender = "m"
            
            self.genders.append(gender)
            self.assertEqual(gender, img['gender'])
            t = time.time() - st
            durations.append(t)
        print('Average detection time: {} s'.format(np.mean(durations)))

    def test_recognition(self):
        durations = []
        for idx_img, img in enumerate(self.test_data):
            st = time.time()
            identities_real = set()
            identities_predicted = set(detection.recognize_faces(self.faces[idx_img]))
            for person in img['people']:
                identities_real.add(person['name'])
            self.assertEqual(identities_predicted, identities_real)
            t = time.time() - st
            durations.append(t)
        print('Average recognition time: {} s'.format(np.mean(durations)))


if __name__ == '__main__':
    unittest.main()
