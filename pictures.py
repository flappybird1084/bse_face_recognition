## Original source from here:
## https://realpython.com/face-detection-in-python-using-a-webcam/

import cv2
import time

video_capture = cv2.VideoCapture(0)
folder = "./img/train/rian/"

counter = 0
while True:
    #print("loop started")
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        print("Exiting...")
        break
    if key  == ord('s'):
        timestr = time.strftime("%Y-%m-%d %H:%M:%S") 
        print("Saving image: "+timestr +"c"+str(counter)+ ".jpeg")
        filename = folder + timestr +"c"+str(counter)+ ".jpeg"
        cv2.imwrite(filename, frame)
        counter=counter+1
    if key == 13: ## enter key
        timestr = time.strftime("%Y-%m-%d %H:%M:%S")
        print("Saving image: "+timestr + ".jpeg")
        filename = folder + timestr + ".jpeg"
        cv2.imwrite(filename, frame)

video_capture.release()
cv2.destroyAllWindows()