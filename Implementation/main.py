from detection.remote import Remote
import detection.detection as detection
import detection.timer as timer

import sys
import os
import time
import cv2

img_path = './test images/faces_sd.jpg'


def main():
    #vid = cv2.VideoCapture(0)
    t = timer.Timer()
    remote = Remote()
    #remote.login()
    while True:
        t.start()
        #ret, img = vid.read()
        #cv2.imwrite('img.jpg', img)
        num_detected, faces = detection.detect_faces_deepface(img_path)
        print('Number of people detected: {}'.format(num_detected))
        print('Currently active users: {}'.format(remote.get_logged_in()))
        if num_detected > len(remote.get_logged_in()):
            print('More people have been detected than are registered. Please log in.')
            #remote.login()
        identities = detection.recognize_faces(faces)
        genders, ages, emotions = detection.analyze_faces(faces)
        for i, _ in enumerate(faces):
            print('{}, {}, {} years old. Dominant emotion: {}'.format(identities[i], genders[i], ages[i], emotions[i]))
        t.stop()
        time.sleep(min(abs(10-t.elapsed_time), 2))


if __name__ == "__main__":
    main()
