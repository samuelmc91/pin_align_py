#!/usr/bin/python3
import os
import sys
import cv2
import argparse
import getpass
import random
import numpy as np
import matplotlib.pyplot as plt

# Gets the directory of where the file is being ran from
if os.getenv('PIN_ALIGN_ROOT') != os.path.dirname(os.path.realpath(__file__)):
    ROOT = os.path.dirname(os.path.realpath(__file__))
    os.environ['PIN_ALIGN_ROOT'] = ROOT
    sys.path.append(ROOT)

from pin_align_config_amx import *

parser = argparse.ArgumentParser(description='Run pin align with 0 and 90 degree images',
                                 epilog='pin_align.sh image_0 image_90 [tilt_limit] ' + 
                                 'compare 0 and 90 degree image writing the resulting pin tip image to image_out')

parser.add_argument('IMG_0', help='Input image at 0 degrees')
parser.add_argument('IMG_90', help='Input image at 90 degrees')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Turn debug mode on')
args = parser.parse_args()

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

def tilt_check(img_0_pin_base, img_90_pin_base):
    alpha = 0.5
    beta = 1.0 - alpha
    combined_img = cv2.addWeighted(img_0_pin_base, alpha, img_90_pin_base, beta, 0)
    tilt_check_top = combined_img[TILT_CHECK_TOP, TILT_CHECK_ROI_WIDTH]
    tilt_check_bottom = combined_img[TILT_CHECK_BOTTOM, TILT_CHECK_ROI_WIDTH]
    plt.imshow(tilt_check_top, cmap='gray')
    
    cv2.imwrite('test_top.jpg', tilt_check_top)
    cv2.imwrite('test_bottom.jpg', tilt_check_bottom)

def pin_check(img_0_pin, img_90_pin):
    pass

fname = args.IMG_0.split('/')[-1]
fbase = fname.split('.')[0]

user_name = getpass.getuser()
tmp_dir = os.path.join(os.getcwd(), user_name + '_pin_align_' + str(random.randint(11111, 99999)))
os.system("mkdir -p " + tmp_dir)
# os.system("chmod 777 " + tmp_dir)

print('0 degree: {}\n90 degree: {}\nFiles in: {}'.format(args.IMG_0, args.IMG_90, tmp_dir))

os.system('cp {} {} {}'.format(args.IMG_0, args.IMG_90, tmp_dir))

img_0 = cv2.imread(os.path.join(tmp_dir, args.IMG_0.split('/')[-1]), 0)
img_90 = cv2.imread(os.path.join(tmp_dir, args.IMG_90.split('/')[-1]), 0)
print(os.path.join(tmp_dir, args.IMG_0.split('/')[-1]))

img_0_pin_tip, img_0_pin_body, img_0_pin_base = pin_align_prep(img_0)
img_90_pin_tip, img_90_pin_body, img_90_pin_base = pin_align_prep(img_90)

cv2.imwrite(os.path.join(tmp_dir, 'img_0_pin_tip.jpg'), img_0_pin_tip)
cv2.imwrite(os.path.join(tmp_dir, 'img_0_pin_body.jpg'), img_0_pin_body)
cv2.imwrite(os.path.join(tmp_dir, 'img_0_pin_base.jpg'), img_0_pin_base)

cv2.imwrite(os.path.join(tmp_dir, 'img_90_pin_tip.jpg'), img_90_pin_tip)
cv2.imwrite(os.path.join(tmp_dir, 'img_90_pin_body.jpg'), img_90_pin_body)
cv2.imwrite(os.path.join(tmp_dir, 'img_90_pin_base.jpg'), img_90_pin_base)

tilt_check(img_0_pin_base, img_90_pin_base)