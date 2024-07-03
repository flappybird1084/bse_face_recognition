#!/bin/bash

python3 camstream_model_both.py &
cd streamlit/
streamlit run Main_Page.py & 