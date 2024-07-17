from message_controller import monitor_for_image
import cv2
from threading import Thread
import time

def display_loop():
    print("display thread started")
    while True:
        print("about to show image")
        try:
            image = cv2.imread("temp/streamlit_detection_image.jpg")
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


