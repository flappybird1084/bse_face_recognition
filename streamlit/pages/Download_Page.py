import streamlit as st
import pandas as pd
import time
from threading import Thread
import os, subprocess

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

st.sidebar.header("Downloads for all compiled videos")

st.button("Refresh")

video_names = []
process = subprocess.Popen(["cd ../detections/videos/ && ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
stdout, stderr = process.communicate()

for i in stdout.split(bytes("\n", encoding="utf8")):
    video_names.append(i.decode())
video_names = video_names[:-1]
print(video_names)

#videos = []
for i in video_names:
    #videos.append(open("../detections/videos/"+i, "rb"))
    st.video(open("../detections/videos/"+i, "rb").read())
    st.download_button(f"Download {i}",open("../detections/videos/"+i, "rb"), i)
    st.write("\n")
    



