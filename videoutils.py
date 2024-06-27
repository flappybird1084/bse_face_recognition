import cv2
import os

def get_avg_diff(inp_list, verbose):
    target_list = []
    for count, i in enumerate(inp_list):
        try:
            target_list.append(inp_list[count+1]-inp_list[count])
        except:
            pass

    avg = 0
    for i in target_list:
        avg += i
    avg = avg/len(target_list)

    if verbose:
        print(avg) # seconds per frame
    # fps is 1/this
    return avg


def compile_video(directory_name, verbose):
    target_fps = 0

    image_folder = 'detections/'+directory_name+"/"
    video_name = 'detections/videos/'+directory_name+'.mp4'

    images = []
    minuteslist = []
    for img in os.listdir(image_folder):
        images.append(img)
        seconds = (int(img[-13:-11]+img[-10:-4])/1000000) #convert filenames into seconds
        if verbose:
            print(img)
        minutes = (seconds+60*int(img[-16:-14])) #converts minutes to seconds
        minuteslist.append(minutes)
    minuteslist = sorted(minuteslist)
    if verbose:
        print(tuple(i for i in minuteslist))
    fps = 1/get_avg_diff(minuteslist, verbose)
    target_fps = fps

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, cv2.VideoWriter.fourcc(*'mp4v'), target_fps, (width,height), True)
    #os.popen("ffmpeg -framerate "+str(target_fps)+"-i "+image_folder+"image-%d.jpg -c:v libx264 -r 30 output.mp4")

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

#compile_video("detection-2024-06-26@16:22:17.826271")