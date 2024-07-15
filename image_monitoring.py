from message_controller import monitor_for_image
import cv2
from threading import Thread

def display_loop():
    while True:
        image = cv2.imread("temp/streamlit_detection_image.jpg")
        cv2.imshow("frame", image)

t = Thread(target=display_loop)
t.run()
while True:
    monitor_for_image("1234")
