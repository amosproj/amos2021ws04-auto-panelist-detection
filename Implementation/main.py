from detection.remote import Remote
import detection.detection as detection
import detection.timer as timer
from registration.register import Register

import sys
import os
import time
import cv2


def main():
    vid = cv2.VideoCapture(0)
    t = timer.Timer()
    remote = Remote()
    remote.login()
    while True:
        r = input("Press r to register a new user, press any other button to skip this")
        if r == 'r':
            Register().register(vid)
        t.start()
        ret, img = vid.read()
        if not ret:
            raise SystemExit('Error occurred while capturing video')
        sys.stdout = open(os.devnull, 'w')
        sys.stdout = sys.__stdout__
        num_detected = detection.detect_faces_deepface(img)
        print('Number of people detected: {}'.format(num_detected))
        print('Currently active users: {}'.format(remote.get_logged_in()))
        if num_detected > len(remote.get_logged_in()):
            print('More people have been detected than are registered. Please log in.')
            remote.login()
        t.stop()
        time.sleep(min(abs(10-t.elapsed_time), 2))


if __name__ == "__main__":
    main()
