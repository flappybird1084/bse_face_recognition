import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader,Dataset
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch.backends.cudnn as cudnn
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
from PIL import Image, ImageDraw
from tempfile import TemporaryDirectory
from facenet_pytorch import MTCNN
import numpy

video_capture = cv2.VideoCapture(0)

model_ft = torch.load("model_ft_5.pt")

device = torch.device('cpu')

mtcnn = MTCNN(keep_all=True, device=device)

def pre_image(model):
    #img = Image.open(image_path)
    _,cv2img = video_capture.read()
    boxes, _ = mtcnn.detect(cv2img)

    color_converted = cv2.cvtColor(cv2img, cv2.COLOR_BGR2RGB) 

    pilcv2img = Image.fromarray(color_converted).copy()
   
    frame_draw = pilcv2img.copy()
    draw = ImageDraw.Draw(frame_draw)


    try:
        for box in boxes:
            draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)
            print(box)
        #frame_draw.show()
        #cv2.imshow("frame2", cv2img)
        #key = cv2.waitKey(1) & 0xff

        cropped_img = pilcv2img.copy()
        cropped_img = cropped_img.crop(boxes[0])
    except:
        print("caught!!")
        cropped_img = pilcv2img.copy()
        

    
    img = frame_draw.copy()
    open_cv_image = numpy.array(img)
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    img2 = frame_draw.copy()
    try:
        img2 = img2.crop(boxes[0])
    except:
        pass
    open_cv_image2 = numpy.array(img2)
    open_cv_image2 = open_cv_image2[:, :, ::-1].copy()



    cv2.imshow("rect-frame", open_cv_image)
    key = cv2.waitKey(1) & 0xff


    mean = [0.485, 0.456, 0.406] 
    std = [0.229, 0.224, 0.225]
    transform_norm = transforms.Compose([transforms.ToTensor(), 
    transforms.Resize((224,224)),transforms.Normalize(mean, std)])
    # get normalized image

    try:
        img_normalized = transform_norm(img.crop(boxes[0])).float()
        img_normalized = img_normalized.unsqueeze_(0)
        # input = Variable(image_tensor)
        img_normalized = img_normalized.to(device)
        # print(img_normalized.shape)
       
    except:
        img_normalized = transform_norm(img).float()
        img_normalized = img_normalized.unsqueeze_(0)
        # input = Variable(image_tensor)
        img_normalized = img_normalized.to(device)
        print("didn't crop")
        # print(img_normalized.shape)

    with torch.no_grad():
        model.eval()  
        output =model(img_normalized)
        print(output)
        index = output.data.cpu().numpy().argmax()
        print(index)
        #classes = train_ds.classes
        #class_name = classes[index]
        #return class_name

_,img = video_capture.read()
#cv2.imshow("Frame",img)

while(True):
    pre_image(model_ft)
    #time.sleep(0.1)
#time.sleep(10)
cv2.waitKey(0)

cv2.destroyAllWindows()
