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
    os.popen("touch temp.txt")
    file = open("temp.txt", "w+")
    message = message
    file.write(message)
    file.close()
    subprocess.Popen("nc "+ip+" "+port+" < temp.txt", stdin=subprocess.PIPE, shell=True)
    #os.popen("rm temp.txt")

def monitor_for_message(port):
    process = subprocess.Popen("nc -l "+port, stdout=subprocess.PIPE,shell=True)
    print(process.stdout.readlines())
        
#transmit_message("nah id win","rianbutala","172.16.9.135", "/home/rianbutala/Desktop/face-recognition/bse_face_recognition", "pipassword")

#transmit_message("nah id lose\n", "172.16.9.135", "1234")

monitor_for_message("1234")

#transmit_message("nah id lose\n", "172.16.4.45", "1234")
