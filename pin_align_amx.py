#!/usr/bin/python3
import os
import sys
import cv2
import argparse
import getpass
import random
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process

# Gets the directory of where the file is being ran from
# if os.getenv('PIN_ALIGN_ROOT') != os.path.dirname(os.path.realpath(__file__)):
#     ROOT = os.path.dirname(os.path.realpath(__file__))
#     os.environ['PIN_ALIGN_ROOT'] = ROOT
#     sys.path.append(ROOT)

ROOT = '/home/samuel/A/pin_align-master/pin_align_py'
os.environ['PIN_ALIGN_ROOT'] = ROOT
sys.path.append(ROOT)

from pin_align_config import *

parser = argparse.ArgumentParser(description='Run pin align with 0 and 90 degree images',
                                 epilog='pin_align.sh image_0 image_90 [tilt_limit] ' +
                                 'compare 0 and 90 degree image writing the resulting pin tip image to image_out')

parser.add_argument('IMG_0', help='Input image at 0 degrees')
parser.add_argument('IMG_90', help='Input image at 90 degrees')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Turn debug mode on')
parser.add_argument('-i', '--image_check', action='store_true',
                    help='Save all crops')
args = parser.parse_args()

fbase_0 = args.IMG_0.split('/')[-1]
fname_0 = fbase_0.split('.')[0]

fbase_90 = args.IMG_90.split('/')[-1]
fname_90 = fbase_90.split('.')[0]

fname_combined = fname_0[:-5] + 'combined' + fname_0[-4:]

user_name = getpass.getuser()
tmp_dir = os.path.join(os.getcwd(), user_name +
                       '_pin_align_' + str(random.randint(11111, 99999)))
os.system("mkdir -p " + tmp_dir)


def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


def pin_align_prep(image_path, fbase, fname):
    fout = os.path.join(tmp_dir, fbase)
    image = cv2.imread(image_path)  # adjust_gamma(cv2.imread(image_path), gamma=0.9)
    cv2.imwrite(os.path.join(tmp_dir, fname + '.jpg'), image)

    # os.system('convert ' + image_path + ' -contrast -contrast ' + fout)
    # os.system('mv {} {}'.format(image_path, fout))

    gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    pin_crops = [[gray_img[DEFAULT_HEIGHT, PIN_TIP], '_pin_tip.jpg'],
                 [gray_img[DEFAULT_HEIGHT, PIN_BODY], '_pin_body.jpg'],
                 [gray_img[DEFAULT_HEIGHT, PIN_BASE], '_pin_base.jpg']]

    images_out = []
    for i in range(len(pin_crops)):
        crop_blur = cv2.GaussianBlur(pin_crops[i][0], (3, 3), 2)
        high_thresh, thresh_im = cv2.threshold(
            crop_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        lowThresh = 0.5*high_thresh
        crop_edge = cv2.Canny(crop_blur, lowThresh, high_thresh)
        crop_bw = cv2.bitwise_not(crop_edge)
        cross_kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
        crop_erode = cv2.erode(crop_bw, cross_kernel, iterations=1)
        crop_dilate = cv2.dilate(crop_erode, cross_kernel, iterations=1)
        images_out.append(crop_dilate)

        cv2.imwrite(os.path.join(tmp_dir, fname +
                                 pin_crops[i][1]), crop_dilate)

        # TODO Save images through processing steps
        if args.image_check:
            pass
            # cv2.imwrite('crop.jpg', crop)
            # cv2.imwrite('crop_blur.jpg', crop_blur)
            # cv2.imwrite('sharpened.jpg', crop_sharpen)
            # cv2.imwrite('high_thresh.jpg', thresh_im)
            # cv2.imwrite('crop_edge.jpg', crop_edge)
            # cv2.imwrite('crop_bw.jpg', crop_bw)
            # cv2.imwrite('crop_erode.jpg', crop_erode)
            # cv2.imwrite('crop_dilate.jpg', crop_dilate)

    return images_out


def tilt_check(img_0_pin_base, img_90_pin_base):
    alpha = 0.5
    beta = 1.0 - alpha
    combined_img = cv2.addWeighted(
        img_0_pin_base, alpha, img_90_pin_base, beta, 0)

    height = TILT_CHECK_TOP_Y2 - TILT_CHECK_TOP_Y1

    tilt_check_x1 = max(PIN_BASE_X1, TILT_CHECK_X1) - \
        min(PIN_BASE_X1, TILT_CHECK_X1)
    tilt_check_x2 = max(PIN_BASE_X2, TILT_CHECK_X2) - \
        min(PIN_BASE_X2, TILT_CHECK_X2)

    if tilt_check_x2 == 0:
        tilt_check_x2 = None

    tilt_check_top_y1 = TILT_CHECK_TOP_Y1 - DEFAULT_ROI_Y1
    tilt_check_top_y2 = tilt_check_top_y1 + height
    tilt_check_top = combined_img[tilt_check_top_y1:
                                  tilt_check_top_y2, tilt_check_x1:tilt_check_x2]
    tilt_top_filename = os.path.join(
        tmp_dir, fname_combined + '_tilt_check_top.jpg')

    tilt_check_bottom_y1 = TILT_CHECK_BOTTOM_Y1 - DEFAULT_ROI_Y1
    tilt_check_bottom_y2 = tilt_check_bottom_y1 + height
    tilt_check_bottom = combined_img[tilt_check_bottom_y1:
                                     tilt_check_bottom_y2, tilt_check_x1:tilt_check_x2]
    tilt_bottom_filename = os.path.join(
        tmp_dir, fname_combined + '_tilt_check_bottom.jpg')

    if args.debug:
        cv2.imwrite(tilt_top_filename, tilt_check_top)
        cv2.imwrite(tilt_bottom_filename, tilt_check_bottom)

    if not np.all(tilt_check_top == 255) or not np.all(tilt_check_bottom == 255):
        print('CAP TILTED')
        sys.exit(0)
    else:
        print('CAP CENTERED')


def pin_check(img_0_pin_body, img_90_pin_body):
    alpha = 0.5
    beta = 1.0 - alpha
    combined_img = cv2.addWeighted(
        img_0_pin_body, alpha, img_90_pin_body, beta, 0)
    height = PIN_CHECK_TOP_Y2 - PIN_CHECK_TOP_Y1

    pin_check_top_y1 = PIN_CHECK_TOP_Y1 - DEFAULT_ROI_Y1
    pin_check_top_y2 = pin_check_top_y1 + height
    pin_check_top = combined_img[pin_check_top_y1:pin_check_top_y2]
    pin_top_filename = os.path.join(
        tmp_dir, fname_combined + '_pin_check_top.jpg')

    pin_check_bottom_y1 = PIN_CHECK_BOTTOM_Y1 - DEFAULT_ROI_Y1
    pin_check_bottom_y2 = pin_check_bottom_y1 + height
    pin_check_bottom = combined_img[pin_check_bottom_y1:pin_check_bottom_y2]
    pin_bottom_filename = os.path.join(
        tmp_dir, fname_combined + '_pin_check_bottom.jpg')

    if args.debug:
        cv2.imwrite(pin_top_filename, pin_check_top)
        cv2.imwrite(pin_bottom_filename, pin_check_bottom)

    # TODO Test Python behavior on empty edge detection vs. Imagemagick
    if not np.all(pin_check_top == 255) or not np.all(pin_check_bottom == 255):
        print('PIN MISSING')
        sys.exit(0)
    elif np.all(img_0_pin_body == 255) or np.all(img_0_pin_body == 255):
        print('PIN MISSING')
        sys.exit(0)
    else:
        print('PIN PRESENT')


def move_to_center(img_0_pin_tip, img_90_pin_tip):
    X1 = 0
    X2 = X1 + (SMALL_BOX_X2 - SMALL_BOX_X1)

    Y1 = SMALL_BOX_Y1 - DEFAULT_ROI_Y1
    Y2 = Y1 + (SMALL_BOX_Y2 - SMALL_BOX_Y1)

    small_box_crop_0 = img_0_pin_tip[Y1:Y2, X1:X2]
    small_box_crop_90 = img_90_pin_tip[Y1:Y2, X1:X2]

    if args.debug:
        box_crop_0_filename = os.path.join(
            tmp_dir, fname_0 + '_pin_box_crop.jpg')
        box_crop_90_filename = os.path.join(
            tmp_dir,  fname_90 + '_pin_box_crop.jpg')
        cv2.imwrite(box_crop_0_filename, small_box_crop_0)
        cv2.imwrite(box_crop_90_filename, small_box_crop_90)

    pixel_location = [False, False]
    black_pixels_0 = []
    black_pixels_90 = []

    for col in range(small_box_crop_0.shape[0]):
        if np.count_nonzero(small_box_crop_0[:, col] == 0) != 0 and not pixel_location[0]:
            # middle_index = np.count_nonzero(small_box_crop_0[:, col] == 0) // 2
            row_0 = np.argwhere(small_box_crop_0[:, col] == 0)[0][0]
            pixel_location[0] = [col, row_0]

        if np.count_nonzero(small_box_crop_90[:, col] == 0) != 0 and not pixel_location[1]:
            # middle_index = np.count_nonzero(small_box_crop_90[:, col] == 0) // 2
            row_90 = np.argwhere(small_box_crop_90[:, col] == 0)[0][0]
            pixel_location[1] = [col, row_90]

        if pixel_location[0] and pixel_location[1]:
            break

    if not pixel_location[0] or not pixel_location[1]:
        print('X Y Z VIOLATION')
        sys.exit(0)
    else:
        print('X, Y, Z WITHIN LIMITS')
    pin_tip_x_0 = SMALL_BOX_X1 + pixel_location[0][0]
    pin_tip_x_90 = SMALL_BOX_X1 + pixel_location[1][0]

    pin_tip_z = SMALL_BOX_Y1 + pixel_location[0][1]
    pin_tip_y = SMALL_BOX_Y1 + pixel_location[1][1]

    pin_tip_x_0_mm = (pin_tip_x_0 - X_CENTER) / DEFAULT_PIXELS_PER_MM

    pin_tip_x_90_mm = (pin_tip_x_90 - X_CENTER) / DEFAULT_PIXELS_PER_MM

    pin_tip_y_mm = (pin_tip_y - Y_CENTER) / DEFAULT_PIXELS_PER_MM
    pin_tip_z_mm = (pin_tip_z - Y_CENTER) / DEFAULT_PIXELS_PER_MM

    if not X_POS:
        pin_tip_x_0_mm = -pin_tip_x_0_mm
        pin_tip_x_90_mm = -pin_tip_x_90_mm
    if not Y_POS:
        pin_tip_y_mm = -pin_tip_y_mm
    if not Z_POS:
        pin_tip_z_mm = -pin_tip_z_mm

    print(
        'OMEGA 0  X,-,Z PIN POS IMAGE2 PX [{}, - , {} ]'.format(pin_tip_x_0, pin_tip_z))
    print(
        'OMEGA 90 X,Y,- PIN POS IMAGE1 PX [{}, {}, - ]'.format(pin_tip_x_90, pin_tip_y))
    print('OVERALL  X,Y,Z PIN POS        PX [{}, {}, {} ]'.format(
        min(pin_tip_x_0, pin_tip_x_90), pin_tip_y, pin_tip_z))

    print('OMEGA 0  X,-,Z OFFSETS TO CENTER IMAGE2 mm [{}, - , {} ]'.format(
        pin_tip_x_0_mm, pin_tip_z_mm))
    print('OMEGA 90 X,Y,- OFFSETS TO CENTER IMAGE1 mm [{}, {}, - ]'.format(
        pin_tip_x_90_mm, pin_tip_y_mm))
    print('OVERALL X,Y,Z OFFSETS TO CENTER         mm [{}, {}, {} ]'.format(
        min(pin_tip_x_0_mm, pin_tip_x_90_mm), pin_tip_y_mm, pin_tip_z_mm))


print('0 degree: {}\n90 degree: {}\nFiles in: {}'.format(
    args.IMG_0, args.IMG_90, tmp_dir))

img_0_pin_tip, img_0_pin_body, img_0_pin_base = pin_align_prep(
    args.IMG_0, fbase_0, fname_0)
img_90_pin_tip, img_90_pin_body, img_90_pin_base = pin_align_prep(
    args.IMG_90, fbase_90, fname_90)

tilt_check(img_0_pin_base, img_90_pin_base)
pin_check(img_0_pin_body, img_90_pin_body)
move_to_center(img_0_pin_tip, img_90_pin_tip)
