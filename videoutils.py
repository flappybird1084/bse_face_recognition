import cv2
import os, subprocess

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
    try:
        target_fps = 0

        image_folder = 'detections/'+directory_name+"/"
        video_name = 'detections/videos/cv'+directory_name+'.mp4'
        final_video_name = 'detections/videos/'+directory_name+'.mp4'
        print(f"Video name: {video_name}. FFMPEG video name: {final_video_name}")

        images = []
        secondslist = []
        for img in os.listdir(image_folder):
            images.append(img)
            seconds = (int(img[-13:-11]+img[-10:-4])/1000000) #convert filenames into seconds
            if verbose:
                print(img)
            minutes = (seconds+60*int(img[-16:-14])) #converts minutes to seconds
            minutes = minutes+60*60*int(img[-19:-17])
            secondslist.append(minutes)
        secondslist = sorted(secondslist)
        if verbose:
            print(tuple(i for i in secondslist))
        fps = 1/get_avg_diff(secondslist, verbose)
        target_fps = fps
        if verbose:
            print("fps generated: "+str(target_fps))

        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape

        video = cv2.VideoWriter(video_name, cv2.VideoWriter.fourcc(*'mp4v'), target_fps, (width,height), True)
        #os.popen("ffmpeg -framerate "+str(target_fps)+"-i "+image_folder+"image-%d.jpg -c:v libx264 -r 30 output.mp4")

        images = sorted(images)
        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()

        print("ffmpeg starting")
        process = subprocess.call(["ffmpeg -i "+video_name+" -vcodec libx264 "+final_video_name], stdout=subprocess.PIPE, shell=True)
        process = subprocess.call(["rm "+video_name], stdout=subprocess.PIPE, shell=True)
        print("ffmpeg ended. video removed.")
    except Exception as e:
        print("critical error!!")
        print(e)

def get_date(filename, verbose):
    index_dash = 0
    index_atsign = 0

    for count, i in enumerate(filename):
        if i == "-" and index_dash == 0:
            index_dash = count
        if i == "@" and index_atsign == 0:
            index_atsign = count

    if verbose:
        print(filename[index_dash+1:index_atsign].split("-")) # 2024, 06, 26: y/m/d

    return (filename[index_dash+1:index_atsign].split("-")) 

def is_file_too_old(baseline, comparison, days, verbose): #with some caveats. for simplicity if year or month doesnt match it says too old. 
    if verbose:
        print(f"checking to see if {comparison} is {days} days older than {baseline}")

    date_baseline = get_date(baseline, verbose)
    date_comparison = get_date(comparison, verbose)

    if int(date_baseline[0]) - int(date_comparison[0]) != 0: #if year is different
        if verbose:
            print ("year mismatch!!")
        return True
    
    if int(date_baseline[1]) - int(date_comparison[1]) != 0: #if month is different
        if verbose:
            print ("month mismatch!!")
        return True
    else:
        is_date_mismatch = int(date_baseline[2]) - int(date_comparison[2]) > days
        if verbose:
            if is_date_mismatch:
                print("date mismatch!!")
            else:
                print("file fits criteria!!")
        return is_date_mismatch

#compile_video("wdetection-2024-07-01@15:04:43.236809", True)
#get_date("detection-2024-06-26@16:22:17.826271")

#print(is_file_too_old("detection-2024-07-01@16:22:17.826271", "detection-2024-06-26@16:22:17.826271", 7, True))

def autoremove_old_files(directory_name, days, verbose):
    process = subprocess.Popen([f"ls {directory_name}"], shell=True, stdout=subprocess.PIPE)

    files = tuple(i.decode()[:-1] for i in process.stdout.readlines()) # old output looked like ('detection-2024-06-01@13:03:18.445190.mp4\n', 'detection-2024-07-01@13:04:49.685851.mp4\n', 'detection-2024-07-01@13:09:39.390657.mp4\n') and had to remove \n

    if verbose:
        print(files)

    for i in files:
        if is_file_too_old(files[-1], i, days, verbose):
            print(f"{i} too old!!")
            os.popen(f"rm {directory_name}{i}")
            print(f"{directory_name}{i} removed!!")

def recompile_video_to_h264(video_name, new_video_name, directory_name): # assume video starts with cvdetection....
    final_video_name = new_video_name
    print("ffmpeg starting")
    process = subprocess.call(["yes | ffmpeg -i "+directory_name+"/"+video_name+" -vcodec libx264 "+directory_name+"/"+final_video_name], stdout=subprocess.PIPE, shell=True)
    process = subprocess.call(["rm "+directory_name+"/"+video_name], stdout=subprocess.PIPE, shell=True)
    print("ffmpeg ended. video removed.")

def recompile_all_cvdetections(directory_name, verbose):
    process = subprocess.Popen([f"ls {directory_name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    stdout = stdout.split(bytes('\n', encoding='utf8'))
    for i in stdout:
        i = i.decode()
        if "cvdetection" in i:
            recompile_video_to_h264(i, i[2:], directory_name)
    if verbose:
        print(stdout)
    

#autoremove_old_files("./detections/videos/", 7, False)
#recompile_all_cvdetections("detections/videos", False)