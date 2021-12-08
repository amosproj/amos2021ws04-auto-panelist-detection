import cv2
import detection.detection as detection
#import image.draw as draw
import image.image as image
import time
import face_recognition




img_path="test images/Samia/samia-liamani-j2tofe0XdUc-unsplash (1).jpg"
img_path2="test images/Samia/samia-liamani-8CFiEezCPfQ-unsplash.jpg"
img_path3="test images/James.jpg"

start = time.time()

known_image = face_recognition.load_image_file(img_path)
unknown_image = face_recognition.load_image_file(img_path2)
print(time.time() - start)



start = time.time()

known_facial_areas = face_recognition.face_locations(known_image)
unknown_facial_areas = face_recognition.face_locations(unknown_image)

print(time.time() - start)
kit_encoding = face_recognition.face_encodings(known_image,known_facial_areas)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image,unknown_facial_areas)[0]
print(time.time() - start)

start = time.time()
results = face_recognition.compare_faces([kit_encoding], unknown_encoding)
print(time.time() - start)
print(results)

