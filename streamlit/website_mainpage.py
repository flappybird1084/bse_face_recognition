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


st.session_state['detection_results'] = "none"

switch = st.toggle("Constantly update image")
update = st.button("Update image")
t = Thread()

image_path = "../temp/streamlit_detection_image.jpg"

image = st.image(image_path)
image2 = st.image(image_path)

image.empty()
image2.empty()

def read_detection_results():
    
    with open("../temp/temp_status_message.txt") as file:
        lines = file.readlines()
        lines.pop(0)
        for count,i in enumerate(lines):
            lines[count] = i[:-1]
        
        st.session_state['detection_results'] = lines
        return lines
    

    
    #writer.join()

def update_image_loop():
    image_path = "../temp/streamlit_detection_image.jpg"

    #image = st.image(image_path)
    #image.empty()
    while True:
        
        st.write(read_detection_results())
        if stop_threads:
            
            break
        display_image()



# if switch: # if on
#     if stop_threads:
#         stop_threads = False
#         t.run()
# else:
#     stop_threads = True
#     try:
#         t.join()
#     except:
#         pass

detection_results_placeholder = st.empty()    


if switch:
    read_detection_results()
    detection_results_placeholder.write(st.session_state['detection_results'])
    while True:
        try:
            image.empty()
            #read_detection_results()
            #st.write(st.session_state['detection_results'])
            image = st.image(image_path)
            time.sleep(0.5)
            read_detection_results()
            detection_results_placeholder.write(st.session_state['detection_results'])
            #st.write(read_detection_results())
        except:
            pass
else:
    read_detection_results()
    st.write(st.session_state['detection_results'])
    #image.empty()
    image = st.image(image_path)


    

#if update:
#    read_detection_results()
#    st.write(st.session_state['detection_results'])
#    #image.empty()
#    image = st.image(image_path)






# t = Thread(target=update_image_loop())




