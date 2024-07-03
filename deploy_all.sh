#!/bin/bash


pyenv shell 3.12.4
nohup python3 camstream_model_both.py --headless &
cd streamlit/
nohup streamlit run Main_Page.py & 