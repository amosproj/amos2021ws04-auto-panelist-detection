from detection.remote import Remote
import detection.detection as detection
import detection.timer as timer

import sys
import os
import time
import cv2

img_path = './img.jpg'


def main():
    vid = cv2.VideoCapture(0)
    t = timer.Timer()
    remote = Remote()
    remote.login()
    while True:
        t.start()
        ret, img = vid.read()
        cv2.imwrite('img.jpg', img)
        sys.stdout = open(os.devnull, 'w')
        sys.stdout = sys.__stdout__
        num_detected = detection.detect_faces_deepface(img_path)
        print('Number of people detected: {}'.format(num_detected))
        print('Currently active users: {}'.format(remote.get_logged_in()))
        if num_detected > len(remote.get_logged_in()):
            print('More people have been detected than are registered. Please log in.')
            remote.login()
        t.stop()
        time.sleep(abs(10-t.elapsed_time))


if __name__ == "__main__":
    main()
