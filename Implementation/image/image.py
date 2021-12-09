import cv2
#from torch._C import namedtuple_a_tau where did this come from kekw


def load(img_path):
    return cv2.imread(img_path)

def save(img,img_path):
    cv2.imwrite(img_path,img)
    return img

def show(img,name="image"):
    cv2.imshow(name, img)
    cv2.waitKey()
    return img


def draw_rectangle(img,roi):
    x,y,w,h = roi
    x, y, w, h = int(x), int(y), int(w), int(h) #facenet fails without this
    color = (255,0,0)
    stroke= 2
    cv2.rectangle(img,(x,y),(w,h),color,stroke)
    return img

def draw_eye_pos(img,roi,eye_pos):
    return NotImplementedError


def write_text(img,roi,text,pos):
    x, y, w, h = roi 
    x, y, w, h = int(x), int(y), int(w), int(h)
    vertical_offset=+5
    horizontal_offset=+12
    cv2.putText(img, text, (w+vertical_offset, y+horizontal_offset*pos), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.6 , (153, 255, 102), 1)
    #cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 1)

    return img

def write_name(img,roi,text):
    return write_text(img,roi,text,1)

def write_age(img,roi,text):
    return write_text(img,roi,text,2)

def write_gender(img,roi,text):
    return write_text(img,roi,text,3)

def write_emotion(img,roi,text):
    return write_text(img,roi,text,4)

def write_attentiveness(img,roi,text):
    return write_text(img,roi,text,5)

def write_ethnicity(img,roi,text):
    return write_text(img,roi,text,6)

def display_info(img,roi,info):
    name = info["name"] if "name" in info else "-"
    gender = info["gender"] if "gender" in info else "-" 
    age = info["age"] if "age" in info else "-" 
    emotion = info["emotion"] if "emotion" in info else "-" 
    attentiveness = info["attentiveness"] if "attentiveness" in info else "-" 
    ethnicity = info["ethnicity"] if "ethnicity" in info else "-" 

    write_name(img,roi,name)
    write_age(img,roi,age)
    write_gender(img,roi,gender)
    write_emotion(img,roi,emotion)
    write_attentiveness(img,roi,attentiveness)
    write_ethnicity(img,roi,ethnicity)
    return img