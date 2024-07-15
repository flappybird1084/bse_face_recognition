from message_controller import monitor_for_image
import cv2

while True:
    monitor_for_image("1234")
    cv2.imshow("frame", "temp/streamlit_detection_image.jpg")
