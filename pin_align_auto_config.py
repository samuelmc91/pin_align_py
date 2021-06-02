#!/usr/bin/python3
import os
import numpy as np
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import sys
import pyautogui
import re
import importlib
from tkinter import ttk

from tool_tip import CreateToolTip
from screen_crop_window import ScreenCrop
import pin_align_config_amx
from pin_align_config_amx import *

global display_help_image_tk
global display_help_image
global on_off_list

pixel_to_mm = 0.2645833333
############### Rect & Edge ###############
on_off_list = [[False, False],
               [False, False],
               [False, False],
               [False, False],
               [False, False],
               [False, False],
               [False, False]]

root = os.getcwd()
config_file_path = os.path.join(root, 'pin_align_config_amx.py')


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
    inputs = importlib.reload(pin_align_config_amx)

    pin_crops = [[inputs.DEFAULT_HEIGHT, inputs.PIN_TIP],
                 [inputs.DEFAULT_HEIGHT, inputs.PIN_BODY],
                 [inputs.DEFAULT_HEIGHT, inputs.PIN_BASE],
                 [inputs.TILT_CHECK_TOP, inputs.TILT_CHECK_ROI_WIDTH],
                 [inputs.TILT_CHECK_BOTTOM, inputs.TILT_CHECK_ROI_WIDTH],
                 [inputs.PIN_CHECK_TOP, inputs.PIN_BODY],
                 [inputs.PIN_CHECK_BOTTOM, inputs.PIN_BODY]]

    return pin_crops


def crop_button_left(event, image_in_canvas, button_choice):
    global on_off_list
    pin_crops = get_pin_crops()
    Y1 = pin_crops[button_choice][0].start
    Y2 = pin_crops[button_choice][0].stop
    X1 = pin_crops[button_choice][1].start
    X2 = pin_crops[button_choice][1].stop

    if button_choice <= 2 and not on_off_list[button_choice][0]:
        new_rect = image_in_canvas.create_crop_rect(X1, Y1, X2, Y2)
        on_off_list[button_choice][0] = new_rect
        print('Y1: {}, Y2: {}, X1: {}, X2: {}'.format(Y1, Y2, X1, X2))
    elif button_choice <= 2 and on_off_list[button_choice][0]:
        image_in_canvas.delete_crop_rect(on_off_list[button_choice][0])
        on_off_list[button_choice][0] = False
    elif button_choice >= 3 and button_choice <= 4 and not on_off_list[button_choice][0]:
        parent_Y1 = pin_crops[2][0].start
        parent_Y2 = pin_crops[2][0].stop
        parent_X1 = pin_crops[2][1].start
        parent_X2 = pin_crops[2][1].stop

        if not on_off_list[2][0]:
            new_rect = image_in_canvas.create_crop_rect(
                parent_X1, parent_Y1, parent_X2, parent_Y2)
            on_off_list[2][0] = new_rect

        new_child_rect = image_in_canvas.create_crop_rect(X1, Y1, X2, Y2)
        on_off_list[button_choice][0] = new_child_rect
        print('Y1: {}, Y2: {}, X1: {}, X2: {}'.format(Y1, Y2, X1, X2))

    elif button_choice >= 3 and button_choice <= 4 and on_off_list[button_choice][0]:
        image_in_canvas.delete_crop_rect(on_off_list[button_choice][0])
        on_off_list[button_choice][0] = False

    elif button_choice >= 5 and not on_off_list[button_choice][0]:
        parent_Y1 = pin_crops[1][0].start
        parent_Y2 = pin_crops[1][0].stop
        parent_X1 = pin_crops[1][1].start
        parent_X2 = pin_crops[1][1].stop

        if not on_off_list[1][0]:
            new_rect = image_in_canvas.create_crop_rect(
                parent_X1, parent_Y1, parent_X2, parent_Y2)
            on_off_list[1][0] = new_rect

        new_child_rect = image_in_canvas.create_crop_rect(X1, Y1, X2, Y2)
        on_off_list[button_choice][0] = new_child_rect
        print('Y1: {}, Y2: {}, X1: {}, X2: {}'.format(Y1, Y2, X1, X2))

    elif button_choice >= 5 and on_off_list[button_choice][0]:
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

    X1 = pin_crops[button_choice][1].start - X
    X2 = pin_crops[button_choice][1].stop - X

    Y1 = 0
    Y2 = pin_crops[button_choice][0].stop - pin_crops[button_choice][0].start

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


def auto_start_button_left(event, image_in_canvas):
    pin_crops = get_pin_crops()
    filename = os.path.join(os.getcwd(), 'display_help_image.jpg')
    X1 = pin_crops[0][1].start
    X2 = pin_crops[2][1].stop

    Y1 = pin_crops[0][0].start
    Y2 = pin_crops[0][0].stop

    width = X2 - X1
    height = Y2 - Y1
    
    current_crop_title.config(text='Points should be as shown', font=('helvetica', 14))
    help_image = image_in_canvas.get_help_image(filename)
    current_crop_label.config(image=help_image)

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


def auto_finished_button_left(event, image_in_canvas):
    X = int(x1_value_in.get())
    Y = int(y1_value_in.get())

    A = int(x2_value_in.get())
    B = int(y2_value_in.get())

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

    if X < A:
        # The cap is on the right and the pin goes to the left
        rtl = True
        X1 = X - 20
        X2 = A + 5
    elif X > A:
        ltr = True
        X1 = A + 5
        X2 = X - 20
    # Y & B should be within x amount of degrees off
    Y1 = Y - 125
    Y2 = Y + 125
    change_config_file(config_file_path, 'DEFAULT_ROI_Y1', Y1)
    change_config_file(config_file_path, 'DEFAULT_ROI_Y2', Y2)

    print('Y1: {}, Y2: {}, X1: {}, X2: {}'.format(Y1, Y2, X1, X2))

    big_box = image_in_canvas.create_big_box(X1, Y1, X2, Y2)

    new_crop = image_in_canvas.get_image(X1, X2, Y1, Y2)
    current_crop_label.config(image=new_crop)
    current_crop_title.config(text='Current Crop', font=('helvetica', 14))

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

    Y_offset = ((Y2 - Y1) // 2) - 25
    # X1 Tilt check
    X_tc = X2 - 50
    change_config_file(config_file_path, 'TILT_CHECK_X1', X_tc)
    change_config_file(config_file_path, 'TILT_CHECK_X2', X2)

    Y1t_tc = Y1 + 25
    Y2t_tc = Y1 + Y_offset
    change_config_file(config_file_path, 'TILT_CHECK_TOP_Y1', Y1t_tc)
    change_config_file(config_file_path, 'TILT_CHECK_TOP_Y2', Y2t_tc)

    Y1b_tc = Y2 - Y_offset
    Y2b_tc = Y2 - 25
    change_config_file(config_file_path, 'TILT_CHECK_BOTTOM_Y1', Y1b_tc)
    change_config_file(config_file_path, 'TILT_CHECK_BOTTOM_Y2', Y2b_tc)

    # Y top Pin check
    Yt_pc = Y1 + Y_offset
    change_config_file(config_file_path, 'PIN_CHECK_TOP_Y1', Y1)
    change_config_file(config_file_path, 'PIN_CHECK_TOP_Y2', Yt_pc)

    Yb_pc = Y2 - Y_offset
    change_config_file(config_file_path, 'PIN_CHECK_BOTTOM_Y1', Yb_pc)
    change_config_file(config_file_path, 'PIN_CHECK_BOTTOM_Y2', Y2)

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
    root.bind('<Motion>', motion)

    w = 1920
    h = 1050

    # get screen width and height
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.title('Pin Align configuration')

    toolbar = tk.Frame(root)
    toolbar.pack(side="top", fill="x")
    ############################ Image Canvas ############################
    image_in_canvas = ScreenCrop(root)

    ############################ Toolbar Canvas ############################

    refresh_button = tk.Button(root, text="Refresh", command=lambda: print(
        'goodbye cruel world'),  bg='green', fg='white', font=10)
    refresh_button.pack(in_=toolbar, side="left", padx=10)

    manual_button = tk.Button(root, text='Manual', command=lambda: image_in_canvas.start_self_crop(),
                              bg='green', fg='white', font=10)
    manual_button.pack(in_=toolbar, side="left", padx=10)

    auto_start_button = tk.Button(
        root, text='Start', bg='green', fg='white', font=10)
    auto_start_button.pack(in_=toolbar, side="left", padx=10)

    auto_finished_button = tk.Button(
        root, text='Finished', bg='green', fg='white', font=10)
    auto_finished_button.pack(in_=toolbar, side="left", padx=10)

    auto_start_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: auto_start_button_left(event, image_in_canvas))
    auto_finished_button.bind(
        "<Button-1>", lambda event, arg=image_in_canvas: auto_finished_button_left(event, image_in_canvas))

    ############################ Current Crop Canvas ############################
    current_crop_canvas = tk.Canvas(root, width=600, height=500,
                                    border=1, relief="sunken")

    n = tk.StringVar()
    pin_length_box = ttk.Combobox(root, width=27, textvariable=n)
    pin_length_box['values'] = [str(i) + ' MM' for i in range(1,21)]
    pin_length_box.current()
    current_crop_canvas.create_window(310, 465, window=pin_length_box)

    pin_length_label = tk.Label(root, text='Select Rod Length')
    pin_length_label.config(font=('helvetica', 14))
    current_crop_canvas.create_window(310, 430, window=pin_length_label)

    whole_crop = image_in_canvas.get_image(
        PIN_TIP_X1, PIN_BASE_X2, DEFAULT_ROI_Y1, DEFAULT_ROI_Y2)

    current_crop_title = tk.Label(root, text='Current Crop')
    current_crop_title.config(font=('helvetica', 14))
    current_crop_canvas.create_window(310, 25, window=current_crop_title)

    current_crop_label = tk.Label(root)
    current_crop_canvas.create_window(310, 250, window=current_crop_label)
    current_crop_label.config(image=whole_crop)
    current_crop_canvas.pack(side="top", fill="both", expand=True)

    ############################ Information Canvas ############################
    information_canvas = tk.Canvas(root, width=600, height=500,
                                   border=1, relief="sunken")

    information_canvas.pack(side="bottom", fill="both", expand=True)

    ############################ Button Settings ############################
    information_canvas_title = tk.Label(text='Select Crop Position')
    information_canvas_title.config(font=('helvetica', 14))
    information_canvas.create_window(300, 15, window=information_canvas_title)

    clear_button = tk.Button(text='Clear', command=lambda: print(
        'clear'), bg='green', fg='white', font=10)
    submit_button = tk.Button(text='Submit', bg='green', fg='white', font=10)
    submit_button.bind("<Button-1>", lambda event,
                       arg=image_in_canvas: crop_button_left(event, image_in_canvas))

    quit_button = tk.Button(
        text='Quit', command=lambda: root.destroy(), bg='green', fg='white', font=10)

    information_canvas.create_window(105, 475, window=clear_button)
    information_canvas.create_window(305, 475, window=submit_button)
    information_canvas.create_window(505, 475, window=quit_button)

    pin_tip_button = tk.Button(text='Pin Tip', bg='green', fg='white', font=10)
    pin_body_button = tk.Button(
        text='Pin Body', bg='green', fg='white', font=10)
    pin_cap_button = tk.Button(text='Pin Cap', bg='green', fg='white', font=10)

    information_canvas.create_window(105, 75, window=pin_tip_button)
    information_canvas.create_window(305, 75, window=pin_body_button)
    information_canvas.create_window(505, 75, window=pin_cap_button)

    tilt_check_top_button = tk.Button(
        text='Tilt Check Top', bg='green', fg='white', font=10)
    tilt_check_bottom_button = tk.Button(
        text='Tilt Check Bottom', bg='green', fg='white', font=10)
    pin_check_top_button = tk.Button(
        text='Pin Check Top', bg='green', fg='white', font=10)
    pin_check_bottom_button = tk.Button(
        text='Pin Check Bottom', bg='green', fg='white', font=10)

    information_canvas.create_window(200, 145, window=tilt_check_top_button)
    information_canvas.create_window(200, 185, window=tilt_check_bottom_button)
    information_canvas.create_window(430, 145, window=pin_check_top_button)
    information_canvas.create_window(430, 185, window=pin_check_bottom_button)

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

    ############################ Y / X Settings ############################
    y1_value_label = tk.Label(root, text='Y1')
    y1_value_label.config(font=('helvetica', 10))
    information_canvas.create_window(450, 310, window=y1_value_label)

    x1_value_label = tk.Label(root, text='X1')
    x1_value_label.config(font=('helvetica', 10))
    information_canvas.create_window(150, 310, window=x1_value_label)

    y1_value_in = tk.Entry(root, justify='center')
    y1_value_in.insert(END, '0')
    y_value_in_ttp = CreateToolTip(y1_value_in, 'Default is 0')
    information_canvas.create_window(450, 345, window=y1_value_in)
    x1_value_in = tk.Entry(root, justify='center')
    x1_value_in.insert(END, '0')
    x_value_in_ttp = CreateToolTip(x1_value_in, 'Default is 0')
    information_canvas.create_window(150, 345, window=x1_value_in)

    ############################ W / X Settings ############################

    # bounding_box = {'top': 248, 'left': 278, 'width': 999, 'height': 185}

    x2_value_label = tk.Label(root, text='X2')
    x2_value_label.config(font=('helvetica', 10))
    information_canvas.create_window(150, 395, window=x2_value_label)

    y2_value_label = tk.Label(root, text='Y2')
    y2_value_label.config(font=('helvetica', 10))
    information_canvas.create_window(450, 395, window=y2_value_label)

    x2_value_in = tk.Entry(root, justify='center')
    x2_value_in.insert(END, '0')
    w_value_in_ttp = CreateToolTip(x2_value_in, 'Default is 0')
    information_canvas.create_window(150, 420, window=x2_value_in)

    y2_value_in = tk.Entry(root, justify='center')
    y2_value_in.insert(END, '0')
    h_value_in_ttp = CreateToolTip(y2_value_in, 'Default is 0')
    information_canvas.create_window(450, 420, window=y2_value_in)

    ############################ Misc Settings ############################

    mouse_pos = Label(root, text='0')
    information_canvas.create_window(310, 275, window=mouse_pos)

    # screen_stream = tk.Label(root)
    # canvas1.create_window(710, 300, window=screen_stream)
    # get_screen(screen_stream)

    # root.after(10, motion)
    root.mainloop()
