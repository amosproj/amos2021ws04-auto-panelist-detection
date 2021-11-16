import cv2

#TODO implement write_name, write_age, draw_gender, draw_eye_pos functions. wrap them in one function

def rectangle(img,roi):
    x,y,w,h = roi
    color = (255,0,0)
    stroke= 2
    cv2.rectangle(img,(x,y),(w,h),color,stroke)
    return img

