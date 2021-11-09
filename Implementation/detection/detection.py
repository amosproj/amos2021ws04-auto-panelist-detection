from cv2 import cv2 # for autocompletion
from insightface.app import FaceAnalysis

def detect_faces(img, show_img):
    app = FaceAnalysis()
    app.prepare(ctx_id=0, det_size=(640, 640))
    faces = app.get(img)
    num_people = len(faces)
    print('Number of people detected: {}'.format(num_people))
    if show_img:
        res = app.draw_on(img, faces)
        cv2.imshow('orig', img)
        cv2.imshow('res', res)
        cv2.waitKey()
    return num_people

_ = detect_faces(cv2.imread('/Users/janis/Desktop/test-img-2.png'), False)
