#!/bin/bash

nohup python3 camstream_model_both.py &
cd streamlit/
nohup streamlit run Main_Page.py & 