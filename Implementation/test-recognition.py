import cv2
import detection.detection as detection
import matplotlib.pyplot as plt
from retinaface import RetinaFace
import os

img_path="test images/Screenshot (131).png"
img = cv2.imread(img_path)
num_detected, faces = detection.detect_faces_deepface(img)

print(num_detected)

identity = detection.recognize_faces(faces)
print(identity)
