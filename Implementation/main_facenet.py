from facenet_pytorch import MTCNN
import torch
import cv2
import image.image as image
import time


#device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')
 
mtcnn = MTCNN(keep_all=True, device=device)
 

start = time.time()

img_path="test images/faces_sd.jpg"
img = cv2.imread(img_path)
frame = img
#frame = cv2.resize(frame, (600, 400))

facial_areas, conf = mtcnn.detect(frame)
print(time.time() - start)


if conf[0] !=  None:
    for facial_area in facial_areas:
        x, y, w, h = facial_area
        x, y, w, h = int(x), int(y), int(w), int(h)
        
        #text = f"{conf[0]*100:.2f}%"

        cv2.putText(frame, "Jon Doe", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 0, 0), 2)
        cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 1)

image.show(frame)
