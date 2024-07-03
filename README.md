# bse_face_recognition
Bluestamp Engineering 2024 Facial Recognition Code Repository

https://flappybird1084.github.io/rianb_BSE_Template_Portfolio/

Setup if you want to try this yourself: <br>
First, ensure you have a virtual environment selected and have the repo cloned. <br>
Then:

```
pip install facenet-pytorch
pip install opencv-python
pip install matplotlib
sudo apt install netcat
```

Enter the right directory (path-to-directory/bse_face_recognition/) and run ```python3 camstream_model_both.py```

If you want to retrain the face recognition go into transfer_learning_main.ipynb and run all the cells up to ```torch.save(xyz.pt)```
If you want to retrain face recognition on your own images: <br>
- Take pictures with pictures.py (hold s to take picture) and specify a directory to save them to
- Clear all files from face_pictures/cropped train and val folders
- Specify a directory in face_tracking.ipynb and run all the cells (crops all images and saves cropped faces to cropped folder
- Then rerun transfer_learning_main.ipynb (make sure to specify a device to train on, like 'cpu', 'mps' (apple gpu) or 'cuda'.

Cool stuff I learned:
- pgrep -a python3 does a grep on only processes named python3 (for killing nohup)
