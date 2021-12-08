import cv2
import time
import image.image as image

face_cascade = cv2.CascadeClassifier('models/cv2_data/haarcascade_frontalface_alt2.xml')

start = time.time()

img_path="test images/Samia/samia-liamani-3lXHHLfYcu0-unsplash.jpg"
img = cv2.imread(img_path)
frame = img

gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)
print(time.time() - start) 


for (x, y, w, h) in faces:
    x, y, w, h = int(x), int(y), int(w), int(h)
    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    
image.show(frame)