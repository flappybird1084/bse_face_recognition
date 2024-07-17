from message_controller import monitor_for_image
import cv2
from threading import Thread
import time
import numpy
from PIL import Image
#from videoutils import resize_cv_image

def convert_cv_to_pil(image):
    color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    pil_image = Image.fromarray(color_coverted) 
    return pil_image

def convert_pil_to_cv(image):
    open_cv_image = numpy.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image


def resize_cv_image(image, newsize):
    image = convert_cv_to_pil(image)
    image = image.resize(size=newsize)
    image = convert_pil_to_cv(image)
    return image


def display_loop():
    print("display thread started")
    while True:
        print("about to show image")
        try:
            image = cv2.imread("temp/streamlit_detection_image.jpg")
            image = resize_cv_image(image, newsize=(400,200))
            cv2.imshow("frame", image)
            print("image shown")
            cv2.waitKey(1)
        except Exception as e:
            print("image not shown")
            print (e)
        
        time.sleep(0.25)


def monitor_loop():
    print("monitor thread started")
    while True:
        print("about to monitor for image")
        monitor_for_image("1235")
        print("image found")
        time.sleep(0.25)


display_thread = Thread(target=display_loop)
monitor_thread = Thread(target=monitor_loop)


monitor_thread.start()
display_thread.run()


