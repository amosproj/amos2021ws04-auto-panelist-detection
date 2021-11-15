import threading
from cv2 import cv2
import time


# https://stackoverflow.com/questions/8600161/executing-periodic-actions
def do_every(period, f, *args):
    def g_tick():
        t = time.time()
        while True:
            t += period
            yield max(t - time.time(), 0)

    g = g_tick()
    while True:
        time.sleep(next(g))
        f(*args)

camera = cv2.VideoCapture(0)  # if 0 does not work try -1,0,1,2,...,

def capture_frame():
    return_value, frame = camera.read()
    print("A picture was taken")
    #cv2.imshow("Laptop Camera Image", frame)  # testing purpose
    #cv2.waitKey(0)
    do_every(10, capture_frame)
    return frame

capture_frame()
# camera.release()
