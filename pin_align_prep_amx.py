import os
import cv2
import sys

if os.getenv('PIN_ALIGN_ROOT') != os.path.dirname(os.path.realpath(__file__)):
    ROOT = os.path.dirname(os.path.realpath(__file__))
    os.environ['PIN_ALIGN_ROOT'] = ROOT
    sys.path.append(ROOT)

from pin_align_config_amx import *

def pin_align_prep(image):
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # image = clahe.apply(image)
    pin_crops = [image[DEFAULT_HEIGHT, PIN_TIP], 
                 image[DEFAULT_HEIGHT, PIN_BODY], 
                 image[DEFAULT_HEIGHT, PIN_BASE]]  
    images_out = []

    for crop in pin_crops:
        crop_blur = cv2.GaussianBlur(crop, (9,9), 2)
        
        high_thresh, thresh_im = cv2.threshold(crop_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        lowThresh = 0.5*high_thresh

        crop_edge = cv2.Canny(crop_blur, lowThresh, high_thresh)
        crop_bw = cv2.bitwise_not(crop_edge)
        
        images_out.append(crop_bw)

    return images_out