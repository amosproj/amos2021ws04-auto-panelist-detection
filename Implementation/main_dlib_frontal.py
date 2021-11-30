import dlib
import cv2
import image.image as image
import time


#face_detect = dlib.cnn_face_detection_model_v1("models/mmod_human_face_detector.dat")
face_detect= dlib.get_frontal_face_detector() # very fast but only detects frontal face 

start = time.time()

img_path="test images/faces_sd.jpg"
img = cv2.imread(img_path)

#img = cv2.resize(img, (600, 400))
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

frame = img

faces = face_detect(frame, 1)

print(time.time() - start) 

for face in faces:
    x1 = face.left()
    y1 = face.bottom()
    x2 = face.right()
    y2 = face.top()
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)

image.show(frame)

