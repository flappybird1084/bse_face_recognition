from message_controller import monitor_for_image
import cv2
from threading import Thread

def display_loop():
    while True:
        image = cv2.imread("temp/streamlit_detection_image.jpg")
        cv2.imshow("frame", image)

def monitor_loop():
    while True:
        monitor_for_image("1234")


display_thread = Thread(target=display_loop)
monitor_thread = Thread(target=monitor_loop)

display_thread.run()
monitor_thread.run()


