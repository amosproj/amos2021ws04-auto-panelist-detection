# redundant but much clearer 

import cv2


def load(img_path):
    return cv2.imread(img_path)

def save(img,img_path):
    cv2.imwrite(img_path,img)
    return img

def show(img,name="image"):
    cv2.imshow(name, img)
    cv2.waitKey()
    return img

