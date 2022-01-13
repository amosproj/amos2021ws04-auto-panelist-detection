from registration.register import Register
from detection.logging import Logger
from detection.remote import Remote
from gui import save_gui

import detection.detection as detection
import detection.timer as timer
import matplotlib.pyplot as plt
import add_family_entry as db
import image.image as image
import image.draw as draw
import torch
import time
import cv2


CAMERA = 1


def main():
    settings = {'register': False}
    print('Panelist detection started.')
    vid = cv2.VideoCapture(CAMERA)
    t = timer.Timer()
    remote = Remote(settings, vid)
    remote.login()
    while True:
        t.start()
        ret, img = vid.read()
        if not ret:
            raise SystemExit('Error occurred while capturing video')
        num_detected, faces = detection.detect_faces_deepface(img)
        print('Number of people detected: {}'.format(num_detected))
        faces_info = detection.detect_faces_RF(img)
        bboxes = detection.get_facial_areas_RF(faces_info)
        if bboxes:
            for i, bbox in enumerate(bboxes):
                if detection.liveness_detector(img, bbox) == True:
                    print('fake face found!')
        identities = detection.recognize_faces(faces)
        genders, ages, emotions = detection.analyze_faces(faces)
        for i, face in enumerate(faces):
            plt.imshow(face)
            if identities[i] == "Unknown":
                print('Not recognized.')
                print('Your gender and age are estimated automatically. If you use this TV frequently, please register '
                      'by pressing "r"')
                id = 0
            else:
                print('Recognized {}'.format(identities[i]))
                id, age, gender = db.get_member(identities[i])
                genders[i] = gender
                ages[i] = age
            # attentiveness = 0 (not implemented)
            Logger.log(id, genders[i], ages[i], emotions[i], 0)

        # print('Currently active users: {}'.format(remote.get_logged_in()))
        # if num_detected > len(remote.get_logged_in()):
        #     print('More people have been detected than are registered. Please log in.')

        if settings['register'] is True:
            Register().register(vid)
            remote.login()
            settings['register'] = False
        t.stop()
        time.sleep(min(abs(10 - t.elapsed_time), 6))


if __name__ == "__main__":
    main()
    # save_gui.main()


def main_2():
    img_path = "test images/faces_sd.jpg"
    img = cv2.imread(img_path)

    faces = detection.detect_faces_RF(img_path)
    facial_areas = detection.get_facial_areas_RF(faces)

    for facial_area in facial_areas:
        img = draw.rectangle(img, facial_area)

    image.show(img, name="faces_sd_detected")
    image.save(img, "test images/faces_sd_detected.jpg")


def main_cv2():
    face_cascade = cv2.CascadeClassifier('models/cv2_data/haarcascade_frontalface_alt2.xml')

    start = time.time()

    img_path = "test images/faces_sd.jpg"
    img = cv2.imread(img_path)
    frame = img

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    print(time.time() - start)

    for (x, y, w, h) in faces:
        x, y, w, h = int(x), int(y), int(w), int(h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    image.show(frame)


def main_dlib_cnn():
    import dlib
    face_detect = dlib.cnn_face_detection_model_v1("models/mmod_human_face_detector.dat")
    # face_detect= dlib.get_frontal_face_detector()

    start = time.time()

    img_path = "test images/faces_sd.jpg"
    img = cv2.imread(img_path)
    frame = img

    faces = face_detect(frame, 1)

    print(time.time() - start)  #

    for face in faces:
        x1 = face.rect.left()
        y1 = face.rect.bottom()
        x2 = face.rect.right()
        y2 = face.rect.top()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)

    image.show(frame)


def main_dlib_frontal():
    import dlib
    # face_detect = dlib.cnn_face_detection_model_v1("models/mmod_human_face_detector.dat")
    face_detect = dlib.get_frontal_face_detector()  # very fast but only detects frontal face

    start = time.time()

    img_path = "test images/faces_sd.jpg"
    img = cv2.imread(img_path)

    # img = cv2.resize(img, (600, 400))
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

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


def main_face_recognition():
    import face_recognition
    img_path = "test images/richard.jpg"
    img_path2 = "test images/richard2.jpg"
    img_path3 = "test images/James.jpg"

    start = time.time()

    known_image = face_recognition.load_image_file(img_path)
    unknown_image = face_recognition.load_image_file(img_path3)
    print(time.time() - start)

    start = time.time()

    known_facial_areas = face_recognition.face_locations(known_image)
    unknown_facial_areas = face_recognition.face_locations(unknown_image)

    print(time.time() - start)
    kit_encoding = face_recognition.face_encodings(known_image, known_facial_areas)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image, unknown_facial_areas)[0]
    print(time.time() - start)

    start = time.time()
    results = face_recognition.compare_faces([kit_encoding], unknown_encoding)
    print(time.time() - start)
    print(results)


def main_facenet():
    from facenet_pytorch import MTCNN
    # device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    device = torch.device('cpu')

    mtcnn = MTCNN(keep_all=True, device=device)

    start = time.time()

    img_path = "test images/faces_sd.jpg"
    img = cv2.imread(img_path)
    frame = img
    # frame = cv2.resize(frame, (600, 400))

    facial_areas, conf = mtcnn.detect(frame)
    print(time.time() - start)

    if conf[0] != None:
        for facial_area in facial_areas:
            x, y, w, h = facial_area
            x, y, w, h = int(x), int(y), int(w), int(h)

            # text = f"{conf[0]*100:.2f}%"

            cv2.putText(frame, "Jon Doe", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 1)

    image.show(frame)
