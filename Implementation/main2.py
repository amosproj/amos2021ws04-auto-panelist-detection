import cv2

import detection.detection as detection
import image.draw as draw
import image.image as image


img_path="test images/faces_sd.jpg"
img = cv2.imread(img_path)


faces = detection.detect_faces_RF(img_path)
facial_areas = detection.get_facial_areas_RF(faces)  

for facial_area in facial_areas:
    img=draw.rectangle(img,facial_area)

image.show(img,name="faces_sd_detected")
image.save(img,"test images/faces_sd_detected.jpg")

