from message_controller import monitor_for_message, monitor_for_image
import subprocess

while True:
    #monitor_for_message("1234")
    monitor_for_image("1234")
    process = subprocess.Popen(["mv streamlit_detection_image_2.jpg streamlit_detection_image.jpg"])
