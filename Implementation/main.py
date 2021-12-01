from registration.register import Register
from detection.remote import Remote
import detection.detection as detection
import detection.timer as timer
from detection.logging import Logger
import matplotlib.pyplot as plt
import addfamilyentry as db

import time
import cv2

CAMERA = 0

def main():
    settings = {'register': False}

    print('Panelist detection started.')
    vid = cv2.VideoCapture(CAMERA)
    t = timer.Timer()
    remote = Remote(settings, vid)
    remote.login()
    while True:
        t.start()
        ret, img = vid.read()
        if not ret:
            raise SystemExit('Error occurred while capturing video')
        num_detected, faces = detection.detect_faces_deepface(img)
        print('Number of people detected: {}'.format(num_detected))
        identities = detection.recognize_faces(faces)
        genders, ages, emotions = detection.analyze_faces(faces)
        for i, face in enumerate(faces):
            plt.imshow(face)
            if identities[i] == "Unknown":
                print('Not recognized.')
                print('Your gender and age are estimated automatically. If you use this TV frequently, please register '
                      'by pressing "r"')
                id = 0
            else:
                print('Recognized {}'.format(identities[i]))
                id, age, gender = db.get_member(identities[i])
                genders[i] = gender
                ages[i] = age
            # attentiveness = 0 (not implemented)
            Logger.log(id, genders[i], ages[i], emotions[i], 0)

        # print('Currently active users: {}'.format(remote.get_logged_in()))
        # if num_detected > len(remote.get_logged_in()):
        #     print('More people have been detected than are registered. Please log in.')

        if settings['register'] is True:
            Register().register(vid)
            remote.login()
            settings['register'] = False
        t.stop()
        time.sleep(min(abs(10-t.elapsed_time), 2))


if __name__ == "__main__":
    main()
