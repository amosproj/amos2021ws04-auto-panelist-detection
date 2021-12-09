import cv2

import detection.detection as detection
import image.image as image


img_path="test images/faces_sd.jpg"
img = cv2.imread(img_path)

# faces = detection.detect_faces_RF(img_path)
# facial_areas = detection.get_facial_areas_RF(faces)

# facial_areas = detection.get_facial_areas_FACENET(img)
# print(facial_areas[0])

# faces = detection.detect_faces_DLIB_FRONTAL(img_path)
# facial_areas = detection.get_facial_areas_DLIB_FRONTAL(faces)

# faces = detection.detect_faces_DLIB_CNN(img_path)
# facial_areas = detection.get_facial_areas_DLIB_CNN(faces)

faces = detection.detect_faces_CV2_CASCADES(img_path)
facial_areas = detection.get_facial_areas_CV2_CASCADES(faces)


for facial_area in facial_areas:
    img=image.draw_rectangle(img,facial_area)


    # *insert recognition models here then fill dictionary with panelist info*
    info=dict()
    info["name"]="Jon Doe"
    info["gender"]="M"
    info["age"]="22"
    #info["ethnicity"]="unknown"
    info["emotion"]="happy"
    info["attentiveness"]="attentive"
    img= image.display_info(img,facial_area,info)
    image.draw_rectangle(img,facial_area)

image.show(img,name="faces_sd_detected")
#image.save(img,"test images/faces_sd_detected.jpg")

#recognition
img_path="test images/richard.jpg" 
img_path2="test images/richard2.jpg" 
print(detection.face_recognition_(img_path,img_path2))