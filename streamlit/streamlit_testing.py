"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import time
from threading import Thread

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


#df = pd.DataFrame({
#  'first column': [1, 2, 3, 4],
#  'second column': [10, 20, 30, 40]
#})

#df

stop_threads = False

switch = st.toggle("Constantly update image")
t = Thread()

def update_image():
    image_path = "../temp/streamlit_detection_image.jpg"

    image2 = st.image(image_path)
    image2.empty()
    while True:

        image = st.image(image_path)
        image2.empty()
        time.sleep(0.5)
        image2 = st.image(image_path)
        image.empty()
        if stop_threads:
            break
    
if switch: # if on
    if stop_threads:
        stop_threads = False
        t.run()
else:
    stop_threads = True
    try:
        t.join()
    except:
        pass

t = Thread(target=update_image())




