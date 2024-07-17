import os, subprocess, time

'''def transmit_message_scp(message, username ,ip , filepath, remotepassword):
    os.popen("touch temp.txt")
    file = open("temp.txt", "w+")
    file.write(message)
    file.close()
    process = subprocess.Popen(("scp temp.txt "+username+"@"+ip+":"+filepath).split(), stdin = subprocess.PIPE)
    process.communicate(bytes(str(remotepassword), encoding='utf8'))
    os.popen("rm temp.txt")'''

def transmit_message(message, ip, port):
    os.popen("cd temp && touch temp_status_message.txt")
    file = open("temp/temp_status_message.txt", "w+")
    message = message
    file.write(message)
    file.close()
    subprocess.Popen("nc "+ip+" "+port+" -w 1 < temp/temp_status_message.txt", stdin=subprocess.PIPE, shell=True)
    #os.popen("rm temp/temp_status_message.txt")

def monitor_for_message(port):
    process = subprocess.Popen("nc -l "+port, stdout=subprocess.PIPE,shell=True)
    read = str(process.stdout.readlines())[3:-4]
    #raw output: [b'message\n']
    print(read) 

def transmit_image(image_path, ip, port):
    subprocess.Popen("nc "+ip+" "+port+" -w 1 < "+image_path, stdin=subprocess.PIPE, shell=True)


def monitor_for_image(port):
    print("debug: monitoring for image")
    process = subprocess.call("nc -l "+port+" > temp/streamlit_detection_image_2.jpg",stdout=subprocess.PIPE, shell = True)
    #lines = process.stdout.readlines()
    #print(f"lines: {lines}")
    print("something happened. hopefully image transfer happened.")
    process = subprocess.call("mv temp/streamlit_detection_image_2.jpg temp/streamlit_detection_image.jpg", shell = True)
    print("file renamed")
   

#transmit_image("temp/streamlit_detection_image.jpg", "172.16.3.32", "1234")
