import cv2

# TODO solve conflicts + delete this file 
def rectangle(img,roi):
    x,y,w,h = roi
    color = (255,0,0)
    stroke= 2
    cv2.rectangle(img,(x,y),(w,h),color,stroke)
    return img