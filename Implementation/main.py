from detection.remote import Remote
import detection.detection as detection

import sys
import os
import time
import cv2


def main():
    remote = Remote()
    remote.login()
    while True:
        img = cv2.imread("C:\\Users\\iyadh\\Desktop\\kit.jpg")
        sys.stdout = open(os.devnull, 'w')
        num_detected = detection.detect_faces(img, False)
        sys.stdout = sys.__stdout__
        print('Number of people detected: {}'.format(num_detected))
        print('Currently active users: {}'.format(remote.get_logged_in()))
        if num_detected > len(remote.get_logged_in()):
            print('More people have been detected than are registered. Please log in.')
            remote.login()
        time.sleep(10)


if __name__ == "__main__":
    main()
