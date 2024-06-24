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

from message_controller import transmit_message

video_capture = cv2.VideoCapture(0)

#model_ft = torch.load("model_ft_5.pt")
model_ft_emotion = torch.load("emotion_model_ft_mps.pt", map_location='cpu')
model_ft_recognition = torch.load("model_ft_5.pt")

#device = torch.device('cpu')
device_emotion = torch.device('cpu')
device_recognition = torch.device('cpu')

mtcnn = MTCNN(keep_all=True, device=torch.device('cpu'))

#TARGET_IP = "172.16.9.135"
TARGET_IP = "172.16.4.45"
TARGET_PORT = "1234"


def get_number_from_tensor(tensor):
    strtensor = str(tensor)
    preprocessed = ""
    for i in strtensor:
        try:
            preprocessed = preprocessed+str(int(i))
        except:
            pass
    preprocessed = preprocessed[:len(preprocessed)-1]
    preprocessed = preprocessed[0] + "." + preprocessed[1:]
    if "-" in strtensor:
        preprocessed = "-"+preprocessed
    return float(preprocessed)

def get_tensor_percentages(class_names, tensor):
    values = []
    for i in tensor[0]:
        values.append(get_number_from_tensor(i))
    #print (tuple(i for i in values))
    lowest = 100
    highest = 0
    for i in values:
        if i < lowest:
            lowest = i
        if i > highest:
            highest = i
    normalized = []
    normalized.append(tuple(i-lowest for i in values))
    #print (tuple(i for i in normalized))
    totalvalue = 0
    for i in normalized[0]:
        totalvalue = totalvalue+i
    percentages = []
    percentages.append(tuple(i/totalvalue for i in normalized[0]))
    #print(totalvalue)
    for count,i in enumerate(percentages[0]):
        print(class_names[count]+" - "+str(i*100)[:5]+"%")
        

def pre_image():

    print("\n")

    #img = Image.open(image_path)
    _,cv2img = video_capture.read()
    boxes, _ = mtcnn.detect(cv2img)

    color_converted = cv2.cvtColor(cv2img, cv2.COLOR_BGR2RGB) 

    pilcv2img = Image.fromarray(color_converted).copy()
   
    frame_draw = pilcv2img.copy()
    draw = ImageDraw.Draw(frame_draw)

    class_names = ["angry" ,"disgust", "fear", "happy", "neutral", "sad", "surprise"]


    try:
        for box in boxes:
            draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)
            #print(box)
        #frame_draw.show()
        #cv2.imshow("frame2", cv2img)
        #key = cv2.waitKey(1) & 0xff

        cropped_img = pilcv2img.copy()
        cropped_img = cropped_img.crop(boxes[0])
    except:
        #print("caught!!")
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

    transform_norm_bw = transforms.Compose([transforms.ToTensor(), 
    transforms.Resize((224,224)),transforms.Normalize([0.456], [0.224])])
    
    try:
        img_normalized = transform_norm(img.crop(boxes[0])).float()
        img_normalized_emotion = transform_norm_bw(img.convert("L").crop(boxes[0])).float()

        img_normalized = img_normalized.unsqueeze_(0)
        # input = Variable(image_tensor)

        #img_normalized_emotion = img_normalized_emotion.to(device_emotion)
        img_normalized_emotion = img_normalized.to(device_emotion)

        img_normalized_recognition = img_normalized.to(device_recognition)

        # print(img_normalized.shape)
       
    except:
        img_normalized = transform_norm(img).float()
        img_normalized_emotion = transform_norm_bw(img.convert("L")).float()


        img_normalized = img_normalized.unsqueeze_(0)
        # input = Variable(image_tensor)
        
        img_normalized_emotion = img_normalized.to(device_emotion)
        img_normalized_recognition = img_normalized.to(device_recognition)

        #print("didn't crop")
        # print(img_normalized.shape)

    with torch.no_grad():
        model_ft_emotion.eval()  
        output =model_ft_emotion(img_normalized_emotion)
        #print(output)
        get_tensor_percentages(class_names, output)
        index = output.data.cpu().numpy().argmax()
        #print(index)
        print("\nmost likely: "+class_names[index])

        #transmit_message(("\nmost likely: "+class_names[index]) + "\n", TARGET_IP, TARGET_PORT)

        #classes = train_ds.classes
        #class_name = classes[index]
        #return class_name

        model_ft_recognition.eval()  
        output =model_ft_recognition(img_normalized_recognition)
        #print(output)
        #get_tensor_percentages(class_names, output)
        index_recognition = output.data.cpu().numpy().argmax()
        print("is rian" if index == 1 else "not rian")
        transmit_message(("\nmost likely: "+class_names[index]+"\n"+"is rian" if index_recognition == 1 else "not rian") +"\n", TARGET_IP, TARGET_PORT)

        #print(index)
        #print("\nmost likely: "+class_names[index])
        #classes = train_ds.classes
        #class_name = classes[index]
        #return class_name

_,img = video_capture.read()
#cv2.imshow("Frame",img)

while(True):
    pre_image()
    #time.sleep(0.1)
#time.sleep(10)
cv2.waitKey(0)

cv2.destroyAllWindows()