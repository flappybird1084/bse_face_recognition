import cv2
import os


def compile_video(directory_name):
    target_fps = 0

    image_folder = 'detections/'+directory_name
    video_name = 'video.mp4'

    images = []
    minuteslist = []
    for img in os.listdir(image_folder):
        images.append(img)
        seconds = (int(img[-13:-11]+img[-10:-4])/1000000) #convert filenames into seconds
        print(img)
        minutes = (seconds+60*int(img[-16:-14])) #converts minutes to seconds
        minuteslist.append(minutes)
    minuteslist = sorted(minuteslist)
    print(tuple(i for i in minuteslist))

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(
        video_name,
        0,
        target_fps,
        (width,height)
    )

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

compile_video("detection-2024-06-26@16:22:17.826271")