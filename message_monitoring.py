from message_controller import monitor_for_message, monitor_for_image
import subprocess, numpy, cv2
from PIL import Image, ImageDraw, ImageFont


def convert_cv_to_pil(image):
    color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    pil_image = Image.fromarray(color_coverted) 
    return pil_image

def convert_pil_to_cv(image):
    open_cv_image = numpy.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    return open_cv_image


def resize_cv_image(image, newsize):
    image = convert_cv_to_pil(image)
    image = image.resize(size=newsize)
    image = convert_pil_to_cv(image)
    return image

while True:
    monitor_for_message("1234")
    with open("temp/temp_status_message.txt", "r") as file:
        read_lines = file.readlines()
    #read_lines = "hello\nyes"
    new_img = Image.new("RGB", (400,100))
    draw_img = new_img.copy()
    draw = ImageDraw.Draw(draw_img)
    font = ImageFont.truetype(r'SimplyMono-Book.ttf',20)
    draw.multiline_text((0,0),read_lines, font=font)
    cv_image = convert_pil_to_cv(draw_img)
    cv2.imshow("frame-message", cv_image)
    cv2.moveWindow("frame-message", 0,400)
    cv2.waitKey(0)
