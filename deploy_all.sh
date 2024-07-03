#!/bin/bash


pyenv shell 3.12.4
nohup python3 camstream_model_both.py --headless &
cd /home/rianbutala/Desktop/face-recognition-pi2/bse_face_recognition/streamlit/ 
nohup streamlit run Main_Page.py & 