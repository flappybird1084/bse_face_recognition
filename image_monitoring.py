from message_controller import monitor_for_image
import cv2

while True:
    image = cv2.imread("temp/streamlit_detection_image.jpg")
    cv2.imshow("frame", image)
    monitor_for_image("1234")
