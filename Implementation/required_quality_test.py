import cv2
import detection.detection as detection
import matplotlib.pyplot as plt
from retinaface import RetinaFace
import os

img_path="test images/Barney/640x360/Screenshot (108).png"
img = cv2.imread(img_path)
num_detected, faces = detection.detect_faces_deepface(img)

# Register someone
#fname="Barney"
#register_path="test images/Barney/640x360/Screenshot (102).png"
#img_register = cv2.imread(register_path)
#face_test = RetinaFace.extract_faces(img_path=img_register, align=True)
#os.mkdir(f'./database/{fname}')
#path=f'./database/{fname}/44.jpg'
#cv2.imwrite(path, face_test[0])


print(num_detected)

identity = detection.recognize_faces(faces)
print(identity)
