#!/usr/bin/python3
import os
import numpy as np
import cv2
import tkinter as tk
import sys
import pyautogui
import re
import importlib

from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk

############### Local Packages ###############
from tool_tip import CreateToolTip
from image_canvas import Image_Canvas
import pin_align_config
from pin_align_config import *
from window_menu_bar import Window_Menu

############### Global Variables ###############
global display_help_image_tk
global display_help_image
global on_off_list
global auto_start_on_off

############### Rect & Edge ###############
on_off_list = [[False, False],  # Pin Tip
               [False, False],  # Pin Body
               [False, False],  # Pin Base
               [False, False],  # Tilt Check Top
               [False, False],  # Tilt Check Bottom
               [False, False],  # Pin Check Top
               [False, False],  # Pin Check Bottom
               [False, False],  # Small Box
               [False, False]]  # Big Box

root = os.getcwd()
config_file_path = os.path.join(root, 'pin_align_config.py')


def update():
    current_pos = 'X: {}\t Y: {}'.format(
        pyautogui.position()[0], pyautogui.position()[1])
    mouse_pos.config(text=current_pos)
    root.after(10, update)


def motion(event):
    x, y = event.x, event.y
    current_pos = 'X: {}\t Y: {}'.format(x, y)
    mouse_pos.config(text=current_pos)
    # root.after(10, motion)


def get_pin_crops():
    inputs = importlib.reload(pin_align_config)

    pin_crops = [[inputs.DEFAULT_HEIGHT, inputs.PIN_TIP],
                 [inputs.DEFAULT_HEIGHT, inputs.PIN_BODY],
                 [inputs.DEFAULT_HEIGHT, inputs.PIN_BASE],
                 [inputs.TILT_CHECK_TOP, inputs.TILT_CHECK_ROI_WIDTH],
                 [inputs.TILT_CHECK_BOTTOM, inputs.TILT_CHECK_ROI_WIDTH],
                 [inputs.PIN_CHECK_TOP, inputs.PIN_BODY],
                 [inputs.PIN_CHECK_BOTTOM, inputs.PIN_BODY],
                 [inputs.SMALL_BOX_HEIGHT, inputs.SMALL_BOX_WIDTH],
                 [inputs.BIG_BOX_HEIGHT, inputs.BIG_BOX_WIDTH],
                 [inputs.X_CENTER, inputs.Y_CENTER],
                 [inputs.INPUT_ROI_WIDTH, inputs.INPUT_ROI_HEIGHT]]

    return pin_crops


def crop_button_left(event, image_in_canvas, button_choice):
    global on_off_list
    pin_crops = get_pin_crops()
    Y1 = pin_crops[button_choice][0].start
    Y2 = pin_crops[button_choice][0].stop
    X1 = pin_crops[button_choice][1].start
    X2 = pin_crops[button_choice][1].stop

    if not on_off_list[button_choice][0]:
        new_rect = image_in_canvas.create_crop_rect(X1, Y1, X2, Y2)
        on_off_list[button_choice][0] = new_rect
        print('Y1: {}, Y2: {}, X1: {}, X2: {}'.format(Y1, Y2, X1, X2))
    elif on_off_list[button_choice][0]:
        image_in_canvas.delete_crop_rect(on_off_list[button_choice][0])
        on_off_list[button_choice][0] = False

    x1_value_in.delete(0, 'end')
    y1_value_in.delete(0, 'end')

    x2_value_in.delete(0, 'end')
    y2_value_in.delete(0, 'end')

    x1_value_in.insert(END, str(X1))
    y1_value_in.insert(END, str(Y1))

    x2_value_in.insert(END, str(X2))
    y2_value_in.insert(END, str(Y2))
    return pin_crops


def crop_button_right(event, image_in_canvas, button_choice):
    global on_off_list
    pin_crops = get_pin_crops()

    X = pin_crops[0][1].start
    Y = pin_crops[0][0].start

    X1 = pin_crops[button_choice][1].start - X
    X2 = pin_crops[button_choice][1].stop - X

    Y1 = pin_crops[button_choice][0].start - Y
    Y2 = Y1 + (pin_crops[button_choice][0].stop -
               pin_crops[button_choice][0].start)

    TOP = pin_crops[button_choice][0].start
    LEFT = pin_crops[button_choice][1].start

    if not on_off_list[button_choice][1]:
        new_edge_crop = image_in_canvas.create_crop_edge(
            X1, X2, Y1, Y2, TOP, LEFT)
        on_off_list[button_choice][1] = new_edge_crop
        print('Y1: {}, Y2: {}, X1: {}, X2: {}'.format(Y1, Y2, X1, X2))
    elif on_off_list[button_choice][1]:
        image_in_canvas.delete_crop_edge(on_off_list[button_choice][1])
        on_off_list[button_choice][1] = False

def clear_image_canvas(image_in_canvas):
    global on_off_list
    on_off_list = image_in_canvas.clear_canvas(on_off_list)

def auto_start_button_left(event, image_in_canvas):
    global help_image_window
    global auto_start_on_off
    clear_image_canvas(image_in_canvas)
    auto_start_on_off = True
    pin_crops = get_pin_crops()
    filename = os.path.join(os.getcwd(), 'display_help_image.jpg')

    current_crop_title.config(
        text='Points should be as shown', font=('helvetica', 14))
    help_image = image_in_canvas.get_help_image(filename)
    help_image_label = tk.Label(root, image=help_image)
    help_image_window = info_canvas_top.create_window(
        310, 250, window=help_image_label)

    pin_tip_button.unbind("<Button-1>")
    pin_body_button.unbind("<Button-1>")
    pin_cap_button.unbind("<Button-1>")
    tilt_check_top_button.unbind("<Button-1>")
    tilt_check_bottom_button.unbind("<Button-1>")
    pin_check_top_button.unbind("<Button-1>")
    pin_check_bottom_button.unbind("<Button-1>")

    pin_tip_button.unbind("<Button-3>")
    pin_body_button.unbind("<Button-3>")
    pin_cap_button.unbind("<Button-3>")
    tilt_check_top_button.unbind("<Button-3>")
    tilt_check_bottom_button.unbind("<Button-3>")
    pin_check_top_button.unbind("<Button-3>")
    pin_check_bottom_button.unbind("<Button-3>")

    pin_tip_button.config(bg='red')
    pin_body_button.config(bg='red')
    pin_cap_button.config(bg='red')
    tilt_check_top_button.config(bg='red')
    tilt_check_bottom_button.config(bg='red')
    pin_check_top_button.config(bg='red')
    pin_check_bottom_button.config(bg='red')

    image_in_canvas.auto_crop_start(y1_value_label, x1_value_label, x2_value_label, y2_value_label,
                                    x1_value_in, y1_value_in, x2_value_in, y2_value_in)


def change_config_file(config_file_path, line_text, new_value):
    lines = open(config_file_path, 'r').readlines()
    line_num = [num for num, f in enumerate(
        lines, 0) if re.findall(line_text, f)][0]
    lines[line_num] = line_text + ' = ' + str(new_value) + '\n'
    out = open(config_file_path, 'w')
    out.writelines(lines)
    out.close()


def auto_submit_button_left(event, image_in_canvas):
    global help_image_window
    global auto_start_on_off
    config_x_cent, config_y_cent = get_pin_crops()[9]
    config_default_width, config_default_height = get_pin_crops()[10]
    rtl = False
    ltr = False
    image_in_canvas.auto_crop_stop(
        y1_value_label, x1_value_label, x2_value_label, y2_value_label)
    change_config_file(config_file_path, 'MIN_X', str(min_x_in.get()))
    change_config_file(config_file_path, 'MIN_Y', str(min_y_in.get()))
    change_config_file(config_file_path, 'MIN_Z', str(min_z_in.get()))

    change_config_file(config_file_path, 'MAX_X', str(max_x_in.get()))
    change_config_file(config_file_path, 'MAX_Y', str(max_y_in.get()))
    change_config_file(config_file_path, 'MAX_Z', str(max_z_in.get()))
    change_config_file(
        config_file_path, 'DEFAULT_PIXELS_PER_MM', str(pixel_per_mm_box.get()))

    rod_length = pin_length_box.get().split(' ')[0]
    change_config_file(config_file_path, 'ROD_LENGTH', rod_length)

    change_config_file(config_file_path, 'X_POS_DIR',
                       str("'" + x_pos_dir_in.get()) + "'")
    change_config_file(config_file_path, 'Y_POS_DIR',
                       str("'" + y_pos_dir_in.get()) + "'")
    change_config_file(config_file_path, 'Z_POS_DIR',
                       str("'" + z_pos_dir_in.get()) + "'")

    if X_POS_DIR == 'LEFT':
        # The cap is on the right and the pin goes to the left
        rtl = True
    elif X_POS_DIR == 'RIGHT':
        ltr = True

    if rtl:
        if auto_start_on_off:
            clear_image_canvas(image_in_canvas)
            X, Y = image_in_canvas.center_pin_image(
                int(x1_value_in.get()), int(y1_value_in.get()))
            height = int(roi_height_in.get()) // 2
            change_config_file(
                config_file_path, 'X_CENTER', str(X))
            change_config_file(
                config_file_path, 'Y_CENTER', str(Y))

            A = int(x2_value_in.get())
            B = Y

            X1 = X + int((pin_align_config.MIN_Z *
                          pin_align_config.DEFAULT_PIXELS_PER_MM))
            X2 = A + 5

            # pixels_pmm = (A - X) // int(rod_length)
            # pixel_per_mm_box.set(pixels_pmm)

            info_canvas_top.delete(help_image_window)
            line = image_in_canvas.draw_new_line(X, Y, A, B)
            try:
                rise = B - Y
                run = A - X
                m = rise / run
                print(m)
                if m > 0.02:
                    print('Pin and glue misaligned, please try again')
            except Exception:
                pass
        elif (config_x_cent != int(x_center_in.get()) or
              config_y_cent != int(y_center_in.get()) or
              config_default_width != int(roi_width_in.get()) or 
              config_default_height != int(roi_height_in.get())):
            clear_image_canvas(image_in_canvas)
            X, Y = int(x_center_in.get()), int(y_center_in.get())
            height = int(roi_height_in.get()) // 2
            
            X1 = X + int((pin_align_config.MIN_Z *
                          pin_align_config.DEFAULT_PIXELS_PER_MM))
            X2 = X1 + int(roi_width_in.get())

            line = image_in_canvas.draw_new_line(X1, Y, X2, Y)
            change_config_file(
                config_file_path, 'X_CENTER', str(x_center_in.get()))
            change_config_file(
                config_file_path, 'Y_CENTER', str(y_center_in.get()))
            change_config_file(config_file_path, 'INPUT_ROI_HEIGHT', str(roi_height_in.get()))
            change_config_file(config_file_path, 'INPUT_ROI_WIDTH', str(roi_width_in.get()))
        else:
            print('Pass')
            return
        # Y & B should be within x amount of degrees off
        Y1 = Y - height
        Y2 = Y + height

        change_config_file(config_file_path, 'DEFAULT_ROI_Y1', Y1)
        change_config_file(config_file_path, 'DEFAULT_ROI_Y2', Y2)

        print('Y1: {}, Y2: {}, X1: {}, X2: {}'.format(Y1, Y2, X1, X2))

        big_box = image_in_canvas.create_big_box(X1, Y1, X2, Y2)
        change_config_file(config_file_path, 'BIG_BOX_X1', X1)
        change_config_file(config_file_path, 'BIG_BOX_X2', X2)
        change_config_file(config_file_path, 'BIG_BOX_Y1', Y1)
        change_config_file(config_file_path, 'BIG_BOX_Y2', Y2)

        small_box = image_in_canvas.create_small_box(X, Y)
        change_config_file(config_file_path, 'BOX_X_IN', X)
        change_config_file(config_file_path, 'BOX_Y_IN', Y)

        new_crop = image_in_canvas.get_image(X1, X2, Y1, Y2)
        current_crop_label.config(image=new_crop)
        current_crop_title.config(
            text='Current Crop', font=('helvetica', 14))

        bbo = (X2 - X1) // 3

        Xt = X1 + bbo
        change_config_file(config_file_path, 'PIN_TIP_X1', X1)
        change_config_file(config_file_path, 'PIN_TIP_X2', Xt)

        Xb = Xt + bbo
        change_config_file(config_file_path, 'PIN_BODY_X1', Xt)
        change_config_file(config_file_path, 'PIN_BODY_X2', Xb)

        Xc = Xb
        change_config_file(config_file_path, 'PIN_BASE_X1', Xc)
        change_config_file(config_file_path, 'PIN_BASE_X2', X2)

        Y_offset = ((Y2 - Y1) // 2) - 35
        # X1 Tilt check
        X_tc = X2 - 50
        change_config_file(config_file_path, 'TILT_CHECK_X1', X_tc)
        change_config_file(config_file_path, 'TILT_CHECK_X2', X2)

        Y1t_tc = Y1 + 20
        Y2t_tc = Y1 + Y_offset
        change_config_file(config_file_path, 'TILT_CHECK_TOP_Y1', Y1t_tc)
        change_config_file(config_file_path, 'TILT_CHECK_TOP_Y2', Y2t_tc)

        Y1b_tc = Y2 - Y_offset
        Y2b_tc = Y2 - 20
        change_config_file(
            config_file_path, 'TILT_CHECK_BOTTOM_Y1', Y1b_tc)
        change_config_file(
            config_file_path, 'TILT_CHECK_BOTTOM_Y2', Y2b_tc)

        # Y top Pin check
        Yt_pc = Y1 + Y_offset
        change_config_file(config_file_path, 'PIN_CHECK_TOP_Y1', Y1)
        change_config_file(config_file_path, 'PIN_CHECK_TOP_Y2', Yt_pc)

        Yb_pc = Y2 - Y_offset
        change_config_file(config_file_path, 'PIN_CHECK_BOTTOM_Y1', Yb_pc)
        change_config_file(config_file_path, 'PIN_CHECK_BOTTOM_Y2', Y2)
        auto_start_on_off = False
    elif ltr:
        print("##### TODO #####")
    else:
        print('pass')

    pin_tip_button.bind("<Button-1>", lambda event,
                        arg=image_in_canvas: crop_button_left(event, image_in_canvas, 0))
    pin_body_button.bind("<Button-1>", lambda event,
                         arg=image_in_canvas: crop_button_left(event, image_in_canvas, 1))
    pin_cap_button.bind("<Button-1>", lambda event,
                        arg=image_in_canvas: crop_button_left(event, image_in_canvas, 2))
    tilt_check_top_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left(event, image_in_canvas, 3))
    tilt_check_bottom_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left(event, image_in_canvas, 4))
    pin_check_top_button.bind("<Button-1>", lambda event,
                              arg=image_in_canvas: crop_button_left(event, image_in_canvas, 5))
    pin_check_bottom_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left(event, image_in_canvas, 6))

    pin_tip_button.bind("<Button-3>", lambda event,
                        arg=image_in_canvas: crop_button_right(event, image_in_canvas, 0))
    pin_body_button.bind("<Button-3>", lambda event,
                         arg=image_in_canvas: crop_button_right(event, image_in_canvas, 1))
    pin_cap_button.bind("<Button-3>", lambda event,
                        arg=image_in_canvas: crop_button_right(event, image_in_canvas, 2))
    tilt_check_top_button.bind(
        "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right(event, image_in_canvas, 3))
    tilt_check_bottom_button.bind(
        "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right(event, image_in_canvas, 4))
    pin_check_top_button.bind("<Button-3>", lambda event,
                              arg=image_in_canvas: crop_button_right(event, image_in_canvas, 5))
    pin_check_bottom_button.bind(
        "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right(event, image_in_canvas, 6))

    pin_tip_button.config(bg='green')
    pin_body_button.config(bg='green')
    pin_cap_button.config(bg='green')
    tilt_check_top_button.config(bg='green')
    tilt_check_bottom_button.config(bg='green')
    pin_check_top_button.config(bg='green')
    pin_check_bottom_button.config(bg='green')


if __name__ == '__main__':
    root = tk.Tk()
    auto_start_on_off = False
    root_menu = Window_Menu(root)
    root.bind('<Motion>', motion)
    toolbar = tk.Frame(root)
    toolbar.pack(side="top", fill="x")

    w = 1920
    h = 1050

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.title('Pin Align configuration')

    ########################### Image Canvas ############################
    image_in_canvas = Image_Canvas(root)

    ########################### Toolbar Canvas ############################
    refresh_button = tk.Button(root, text="Refresh", command=lambda: print(
        'Fix'),  bg='green', fg='white', font=10)
    refresh_button.pack(in_=toolbar, side="left", padx=10)

    manual_button = tk.Button(root, text='Manual', command=lambda: image_in_canvas.start_self_crop(),
                              bg='green', fg='white', font=10)
    manual_button.pack(in_=toolbar, side="left", padx=10)

    clear_button = tk.Button(text='Clear', command=lambda: clear_image_canvas(image_in_canvas), bg='green', fg='white', font=10)
    clear_button.pack(in_=toolbar, side="left", padx=10)

    small_box_button = tk.Button(
        root, text='Small Box', bg='green', fg='white', font=10)
    small_box_button.pack(in_=toolbar, side="left", padx=10)

    small_box_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left(event, image_in_canvas, 7))

    small_box_button.bind(
        "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right(event, image_in_canvas, 7))

    big_box_button = tk.Button(
        root, text='Big Box', bg='green', fg='white', font=10)
    big_box_button.pack(in_=toolbar, side="left", padx=10)

    big_box_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left(event, image_in_canvas, 8))

    big_box_button.bind(
        "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right(event, image_in_canvas, 8))

    ############################ Info Canvas Top ############################
    info_canvas_top = tk.Canvas(root, width=600, height=500,
                                border=1, relief="sunken")

    style = ttk.Style()
    style.map('TCombobox', fieldbackground=[('readonly', 'white')])

    pin_length_label = tk.Label(root, text='Select Rod Length')
    pin_length_label.config(font=('helvetica', 10))

    pin_length_in = tk.StringVar()
    pin_length_box = ttk.Combobox(
        root, width=15, height=10, textvariable=pin_length_in, justify='center')
    pin_length_box['values'] = [str(i) + ' MM' for i in range(1, 21)]
    pin_length_box['state'] = 'readonly'
    pin_length_box.current(17)
    info_canvas_top.create_window(90, 315, window=pin_length_label)
    info_canvas_top.create_window(90, 335, window=pin_length_box)

    pixel_per_mm_label = tk.Label(root, text='Set Pixel per MM')
    pixel_per_mm_label.config(font=('helvetica', 10))

    pixel_per_mm_in = tk.StringVar()
    pixel_per_mm_box = ttk.Combobox(
        root, width=15, height=10, textvariable=pixel_per_mm_in, justify='center')
    pixel_per_mm_box['values'] = [str(i) for i in range(1, 26)]
    pixel_per_mm_box['state'] = 'readonly'
    pixel_per_mm_box.current(DEFAULT_PIXELS_PER_MM - 1)
    info_canvas_top.create_window(310, 315, window=pixel_per_mm_label)
    info_canvas_top.create_window(310, 335, window=pixel_per_mm_box)

    roi_width_label = tk.Label(root, text='Total Width')
    roi_width_label.config(font=('helvetica', 10))
    roi_width_in = tk.Entry(root, justify='center', width=15)
    roi_width_in.insert(END, str(INPUT_ROI_WIDTH))
    info_canvas_top.create_window(520, 315, window=roi_width_label)
    info_canvas_top.create_window(520, 335, window=roi_width_in)

    x_center_label = tk.Label(root, text='X Center Point')
    x_center_label.config(font=('helvetica', 10))
    x_center_in = tk.Entry(root, justify='center', width=15)
    x_center_in.insert(END, str(X_CENTER))
    info_canvas_top.create_window(90, 390, window=x_center_label)
    info_canvas_top.create_window(90, 410, window=x_center_in)

    y_center_label = tk.Label(root, text='Y Center Point')
    y_center_label.config(font=('helvetica', 10))
    y_center_in = tk.Entry(root, justify='center', width=15)
    y_center_in.insert(END, str(Y_CENTER))
    info_canvas_top.create_window(310, 390, window=y_center_label)
    info_canvas_top.create_window(310, 410, window=y_center_in)

    roi_height_label = tk.Label(root, text='ROI Height')
    roi_height_label.config(font=('helvetica', 10))
    roi_height_in = tk.Entry(root, justify='center', width=15)
    roi_height_in.insert(END, str(INPUT_ROI_HEIGHT))
    info_canvas_top.create_window(520, 390, window=roi_height_label)
    info_canvas_top.create_window(520, 410, window=roi_height_in)

    x_pos_dir_label = tk.Label(root, text='X Positive Direction')
    x_pos_dir_label.config(font=('helvetica', 10))
    x_pos_dir_in = tk.StringVar()
    x_pos_dir_box = ttk.Combobox(
        root, width=15, height=10, textvariable=x_pos_dir_in, justify='center')
    x_pos_dir_box['values'] = ['LEFT', 'RIGHT']
    x_pos_dir_box['state'] = 'readonly'
    x_pos_dir_box.set(str(X_POS_DIR))
    info_canvas_top.create_window(90, 465, window=x_pos_dir_label)
    info_canvas_top.create_window(90, 485, window=x_pos_dir_box)

    y_pos_dir_label = tk.Label(root, text='Y Positive Direction')
    y_pos_dir_label.config(font=('helvetica', 10))
    y_pos_dir_in = tk.StringVar()
    y_pos_dir_box = ttk.Combobox(
        root, width=15, height=10, textvariable=y_pos_dir_in, justify='center')
    y_pos_dir_box['values'] = ['UP', 'DOWN']
    y_pos_dir_box['state'] = 'readonly'
    y_pos_dir_box.set(str(Y_POS_DIR))
    info_canvas_top.create_window(310, 465, window=y_pos_dir_label)
    info_canvas_top.create_window(310, 485, window=y_pos_dir_box)

    z_pos_dir_label = tk.Label(root, text='Z Positive Direction')
    z_pos_dir_label.config(font=('helvetica', 10))
    z_pos_dir_in = tk.StringVar()
    z_pos_dir_box = ttk.Combobox(
        root, width=15, height=10, textvariable=z_pos_dir_in, justify='center')
    z_pos_dir_box['values'] = ['UP', 'DOWN']
    z_pos_dir_box['state'] = 'readonly'
    z_pos_dir_box.set(str(Z_POS_DIR))
    info_canvas_top.create_window(520, 465, window=z_pos_dir_label)
    info_canvas_top.create_window(520, 485, window=z_pos_dir_box)

    current_crop_title = tk.Label(root, text='Current Crop')
    current_crop_title.config(font=('helvetica', 14))
    info_canvas_top.create_window(310, 25, window=current_crop_title)

    whole_crop = image_in_canvas.get_image(
        BIG_BOX_X1, BIG_BOX_X2, BIG_BOX_Y1, BIG_BOX_Y2)
    current_crop_label = tk.Label(root)
    info_canvas_top.create_window(310, 160, window=current_crop_label)
    current_crop_label.config(image=whole_crop)
    info_canvas_top.pack(side="top", fill="both", expand=True)
    info_canvas_top.create_line(0, 295, 600, 295, fill='black', width=1)
    ############################ Min Labels & Entry ############################

    min_x_label = tk.Label(root, text='Min X')
    min_x_label.config(font=('helvetica', 14))
    min_x_in = tk.Entry(root, justify='center', width=10)
    min_x_in.insert(END, str(MIN_X))
    info_canvas_top.create_window(90, 25, window=min_x_label)
    info_canvas_top.create_window(90, 45, window=min_x_in)

    min_y_label = tk.Label(root, text='Min Y')
    min_y_label.config(font=('helvetica', 14))
    min_y_in = tk.Entry(root, justify='center', width=10)
    min_y_in.insert(END, str(MIN_Y))
    info_canvas_top.create_window(90, 125, window=min_y_label)
    info_canvas_top.create_window(90, 145, window=min_y_in)

    min_z_label = tk.Label(root, text='Min Z')
    min_z_label.config(font=('helvetica', 14))
    min_z_in = tk.Entry(root, justify='center', width=10)
    min_z_in.insert(END, str(MIN_Z))
    info_canvas_top.create_window(90, 225, window=min_z_label)
    info_canvas_top.create_window(90, 245, window=min_z_in)

    ############################ Max Labels & Entry ############################

    max_x_label = tk.Label(root, text='Max X')
    max_x_label.config(font=('helvetica', 14))
    max_x_in = tk.Entry(root, justify='center', width=10)
    max_x_in.insert(END, str(MAX_X))
    info_canvas_top.create_window(525, 25, window=max_x_label)
    info_canvas_top.create_window(525, 45, window=max_x_in)

    max_y_label = tk.Label(root, text='Max Y')
    max_y_label.config(font=('helvetica', 14))
    max_y_in = tk.Entry(root, justify='center', width=10)
    max_y_in.insert(END, str(MAX_Y))
    info_canvas_top.create_window(525, 125, window=max_y_label)
    info_canvas_top.create_window(525, 145, window=max_y_in)

    max_z_label = tk.Label(root, text='Max Z')
    max_z_label.config(font=('helvetica', 14))
    max_z_in = tk.Entry(root, justify='center', width=10)
    max_z_in.insert(END, str(MAX_Z))
    info_canvas_top.create_window(525, 225, window=max_z_label)
    info_canvas_top.create_window(525, 245, window=max_z_in)

    ############################ Info Canvas Bottom ############################
    info_canvas_bottom = tk.Canvas(root, width=600, height=500,
                                   border=1, relief="sunken")

    info_canvas_bottom.pack(side="bottom", fill="both", expand=True)

    info_canvas_bottom.create_line(0, 250, 600, 250, fill='black', width=1)

    info_bottom_title = tk.Label(text='Select Crop Position')
    info_bottom_title.config(font=('helvetica', 14))
    info_canvas_bottom.create_window(300, 15, window=info_bottom_title)

    auto_start_button = tk.Button(
        text='Start', bg='green', fg='white', font=10)

    auto_submit_button = tk.Button(
        text='Submit', bg='green', fg='white', font=10)

    auto_start_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: auto_start_button_left(event, image_in_canvas))
    auto_submit_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: auto_submit_button_left(event, image_in_canvas))

    quit_button = tk.Button(
        text='Quit', command=lambda: root.destroy(), bg='green', fg='white', font=10)

    info_canvas_bottom.create_window(105, 475, window=auto_start_button)
    info_canvas_bottom.create_window(305, 475, window=auto_submit_button)
    info_canvas_bottom.create_window(505, 475, window=quit_button)

    pin_tip_button = tk.Button(text='Pin Tip', bg='green', fg='white', font=10)
    pin_body_button = tk.Button(
        text='Pin Body', bg='green', fg='white', font=10)
    pin_cap_button = tk.Button(text='Pin Cap', bg='green', fg='white', font=10)

    info_canvas_bottom.create_window(105, 75, window=pin_tip_button)
    info_canvas_bottom.create_window(305, 75, window=pin_body_button)
    info_canvas_bottom.create_window(505, 75, window=pin_cap_button)

    tilt_check_top_button = tk.Button(
        text='Tilt Check Top', bg='green', fg='white', font=10)
    tilt_check_bottom_button = tk.Button(
        text='Tilt Check Bottom', bg='green', fg='white', font=10)
    pin_check_top_button = tk.Button(
        text='Pin Check Top', bg='green', fg='white', font=10)
    pin_check_bottom_button = tk.Button(
        text='Pin Check Bottom', bg='green', fg='white', font=10)

    info_canvas_bottom.create_window(200, 145, window=pin_check_top_button)
    info_canvas_bottom.create_window(200, 185, window=pin_check_bottom_button)
    info_canvas_bottom.create_window(430, 145, window=tilt_check_top_button)
    info_canvas_bottom.create_window(430, 185, window=tilt_check_bottom_button)

    pin_tip_button.bind("<Button-1>", lambda event,
                        arg=image_in_canvas: crop_button_left(event, image_in_canvas, 0))
    pin_body_button.bind("<Button-1>", lambda event,
                         arg=image_in_canvas: crop_button_left(event, image_in_canvas, 1))
    pin_cap_button.bind("<Button-1>", lambda event,
                        arg=image_in_canvas: crop_button_left(event, image_in_canvas, 2))
    tilt_check_top_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left(event, image_in_canvas, 3))
    tilt_check_bottom_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left(event, image_in_canvas, 4))
    pin_check_top_button.bind("<Button-1>", lambda event,
                              arg=image_in_canvas: crop_button_left(event, image_in_canvas, 5))
    pin_check_bottom_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: crop_button_left(event, image_in_canvas, 6))

    pin_tip_button.bind("<Button-3>", lambda event,
                        arg=image_in_canvas: crop_button_right(event, image_in_canvas, 0))
    pin_body_button.bind("<Button-3>", lambda event,
                         arg=image_in_canvas: crop_button_right(event, image_in_canvas, 1))
    pin_cap_button.bind("<Button-3>", lambda event,
                        arg=image_in_canvas: crop_button_right(event, image_in_canvas, 2))
    tilt_check_top_button.bind(
        "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right(event, image_in_canvas, 3))
    tilt_check_bottom_button.bind(
        "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right(event, image_in_canvas, 4))
    pin_check_top_button.bind("<Button-3>", lambda event,
                              arg=image_in_canvas: crop_button_right(event, image_in_canvas, 5))
    pin_check_bottom_button.bind(
        "<Button-3>", lambda event, arg=image_in_canvas: crop_button_right(event, image_in_canvas, 6))

    ############################ Y1 / X1 Settings ############################
    y1_value_label = tk.Label(root, text='Y1')
    y1_value_label.config(font=('helvetica', 14))
    info_canvas_bottom.create_window(450, 310, window=y1_value_label)

    x1_value_label = tk.Label(root, text='X1')
    x1_value_label.config(font=('helvetica', 14))
    info_canvas_bottom.create_window(150, 310, window=x1_value_label)

    y1_value_in = tk.Entry(root, justify='center')
    y1_value_in.insert(END, '0')
    y_value_in_ttp = CreateToolTip(y1_value_in, 'Default is 0')
    info_canvas_bottom.create_window(450, 345, window=y1_value_in)
    x1_value_in = tk.Entry(root, justify='center')
    x1_value_in.insert(END, '0')
    x_value_in_ttp = CreateToolTip(x1_value_in, 'Default is 0')
    info_canvas_bottom.create_window(150, 345, window=x1_value_in)

    ############################ X2 / Y2 Settings ############################
    x2_value_label = tk.Label(root, text='X2')
    x2_value_label.config(font=('helvetica', 14))
    info_canvas_bottom.create_window(150, 395, window=x2_value_label)

    y2_value_label = tk.Label(root, text='Y2')
    y2_value_label.config(font=('helvetica', 14))
    info_canvas_bottom.create_window(450, 395, window=y2_value_label)

    x2_value_in = tk.Entry(root, justify='center')
    x2_value_in.insert(END, '0')
    w_value_in_ttp = CreateToolTip(x2_value_in, 'Default is 0')
    info_canvas_bottom.create_window(150, 420, window=x2_value_in)

    y2_value_in = tk.Entry(root, justify='center')
    y2_value_in.insert(END, '0')
    h_value_in_ttp = CreateToolTip(y2_value_in, 'Default is 0')
    info_canvas_bottom.create_window(450, 420, window=y2_value_in)

    ############################ Misc Settings ############################

    mouse_pos = Label(root, text='0')
    info_canvas_bottom.create_window(310, 275, window=mouse_pos)

    # screen_stream = tk.Label(root)
    # canvas1.create_window(710, 300, window=screen_stream)
    # get_screen(screen_stream)

    # root.after(10, motion)
    root.mainloop()
