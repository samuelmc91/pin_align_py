import os
import numpy as np
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import sys


class Image_Canvas():
    def __init__(self, master):
        self.master = master
        self.x = self.y = 0
        self.curX = self.curY = 0
        self.im_in = cv2.imread(sys.argv[1], 0)
        self.im_height, self.im_width = self.im_in.shape

        self.show_crop = None
        self.new_crop_edges = None
        self.whole_crop = None
        self.rect = None
        self.start_x = None
        self.start_y = None

        self.self_crop_on = False
        self.auto_crop_on = False
        self.line = False
        self.big_box = False
        self.small_box = False
        self.oval_list = [False, False]

        self.crop_edge_list = []
        self.oval_count = 0

        self.screen_canvas = Canvas(
            self.master, width=self.im_width, height=self.im_height, border=1, relief="sunken")
        self.screen_canvas.pack(side="left", fill="both", expand=True)

        self.im = Image.fromarray(self.im_in)
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.screen_canvas.create_image(0, 0, anchor='nw', image=self.tk_im)

    def get_image(self, X1, X2, Y1, Y2):
        image = self.im_in[Y1:Y2, X1:X2]
        image_blur = cv2.GaussianBlur(image, (9, 9), 2)
        high_thresh, thresh_im = cv2.threshold(
            image_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        lowThresh = 0.5*high_thresh

        image_edge = cv2.Canny(image_blur, lowThresh, high_thresh)
        self.image_bw = cv2.bitwise_not(image_edge)
        img = Image.fromarray(self.image_bw)

        self.whole_crop = ImageTk.PhotoImage(img)
        return self.whole_crop

    def get_help_image(self, filename):
        display_help_image_in = cv2.imread(filename)
        display_help_image = Image.fromarray(display_help_image_in)
        self.display_help_image_tk = ImageTk.PhotoImage(display_help_image)
        return self.display_help_image_tk

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.screen_canvas.create_rectangle(
                self.x, self.y, 1, 1, fill="", outline='red')

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.screen_canvas.coords(self.rect, self.start_x,
                                  self.start_y, self.curX, self.curY)

    def reset_window(self):
        self.screen_canvas.delete(self.rect)
        # self.current_crop_canvas.destroy()

    def on_button_release(self, event):
        print(self.rect, self.start_x, self.start_y, self.curX, self.curY)
        pass

    def create_crop_rect(self, X1, Y1, X2, Y2):
        if self.oval_list:
            for circle in self.oval_list:
                self.screen_canvas.delete(circle)
        if self.line:
            self.screen_canvas.delete(self.line)
        if self.big_box:
            self.screen_canvas.delete(self.big_box)
        if self.small_box:
            self.screen_canvas.delete(self.small_box)

        self.show_crop = self.screen_canvas.create_rectangle(
            X1, Y1, X2, Y2, fill='', outline='red')
        return self.show_crop

    def create_big_box(self, X1, Y1, X2, Y2):
        self.big_box = self.screen_canvas.create_rectangle(
            X1, Y1, X2, Y2, fill='', outline='red')

    def create_small_box(self, X, Y):
        X1 = X - 15
        X2 = X + 15
        Y1 = Y - 15
        Y2 = Y + 15
        self.small_box = self.screen_canvas.create_rectangle(
            X1, Y1, X2, Y2, fill='', outline='red')

    def center_pin_image(self, X, Y):
        X1 = X - 15
        X2 = X + 15
        Y1 = Y - 15
        Y2 = Y + 15

        self.get_image(X1, X2, Y1, Y2)
        small_box_edge = self.image_bw

        for col in range(small_box_edge.shape[0]):
            black_pixels = []
            if 0 in small_box_edge[:, col]:
                for row in range(len(small_box_edge[:, col])):
                    if small_box_edge[row, col] == 0:
                        black_pixels.append([col,row])
            if len(black_pixels) >= 3:
                middle_index = len(black_pixels) // 2
                pixel_location = black_pixels[middle_index]
                break

        print(pixel_location)
        new_x = X + (pixel_location[0] - 15)
        new_y = Y + (pixel_location[1] - 15)

        return [new_x, new_y]

    def delete_crop_rect(self, rect):
        self.screen_canvas.delete(rect)

    def start_self_crop(self):
        if self.self_crop_on:
            self.screen_canvas.config(cursor='')
            self.screen_canvas.unbind("<ButtonPress-1>")
            self.screen_canvas.unbind("<B1-Motion>")
            self.screen_canvas.unbind("<ButtonRelease-1>")
            self.self_crop_on = False
        elif not self.self_crop_on:
            self.screen_canvas.config(cursor='cross')
            self.screen_canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.screen_canvas.bind("<B1-Motion>", self.on_move_press)
            self.screen_canvas.bind(
                "<ButtonRelease-1>", self.on_button_release)
            self.self_crop_on = True

    def create_crop_edge(self, X1, X2, Y1, Y2, TOP, LEFT):
        new_image = self.image_bw[Y1:Y2, X1:X2]
        # X1 = 410 = 0
        # X2 = 690 = 280

        img = Image.fromarray(new_image)
        self.new_crop_edges = ImageTk.PhotoImage(img)
        crop_edge = self.screen_canvas.create_image(
            LEFT, TOP, image=self.new_crop_edges, anchor='nw')
        self.crop_edge_list.append(self.new_crop_edges)
        return crop_edge

    def delete_crop_edge(self, crop_edge):
        # crop_edge_index = self.crop_edge_list.index(crop_edge)
        # self.crop_edge_list.pop(crop_edge_index)
        self.screen_canvas.delete(crop_edge)

    def auto_crop_start(self, y1_value_label, x1_value_label, x2_value_label, y2_value_label,
                        x1_value_in, y1_value_in, x2_value_in, y2_value_in):
        if self.auto_crop_on:
            self.auto_crop_stop(y1_value_label, x1_value_label,
                                x2_value_label, y2_value_label)
        elif not self.auto_crop_on:
            self.screen_canvas.config(cursor='cross')
            self.screen_canvas.bind("<ButtonPress-1>", lambda event: self.auto_crop_press(
                event, x1_value_in, y1_value_in, x2_value_in, y2_value_in))
            x1_value_label.config(text='Pin X', font=('helvetica', 10))
            y1_value_label.config(text='Pin Y', font=('helvetica', 10))
            x2_value_label.config(text='Glue X', font=('helvetica', 10))
            y2_value_label.config(text='Glue Y', font=('helvetica', 10))
            self.auto_crop_on = True

    def auto_crop_stop(self, y1_value_label, x1_value_label, x2_value_label, y2_value_label):
        self.screen_canvas.config(cursor='')
        self.screen_canvas.unbind("<ButtonPress-1>")
        x1_value_label.config(text='X1', font=('helvetica', 10))
        y1_value_label.config(text='Y1', font=('helvetica', 10))
        x2_value_label.config(text='X2', font=('helvetica', 10))
        y2_value_label.config(text='Y2', font=('helvetica', 10))
        self.auto_crop_on = False

    def auto_crop_press(self, event, x1_value_in, y1_value_in, x2_value_in, y2_value_in):
        self.auto_press_x = event.x
        self.auto_press_y = event.y
        radius = 10

        X1 = self.auto_press_x - radius
        Y1 = self.auto_press_y - radius
        X2 = self.auto_press_x + radius
        Y2 = self.auto_press_y + radius

        if self.oval_count == 0:
            if self.oval_list[0]:
                self.screen_canvas.delete(self.oval_list[self.oval_count])
            self.new_circle = self.screen_canvas.create_oval(
                X1, Y1, X2, Y2, fill='green')
            self.oval_list[0] = self.new_circle
            self.oval_count = 1
            x1_value_in.delete(0, 'end')
            y1_value_in.delete(0, 'end')
            x1_value_in.insert(END, str(X1 + radius))
            y1_value_in.insert(END, str(Y1 + radius))
        elif self.oval_count == 1:
            if self.oval_list[1]:
                self.screen_canvas.delete(self.oval_list[self.oval_count])
            self.new_circle = self.screen_canvas.create_oval(
                X1, Y1, X2, Y2, fill='blue')
            self.oval_list[1] = self.new_circle
            self.oval_count = 0
            x2_value_in.delete(0, 'end')
            y2_value_in.delete(0, 'end')
            x2_value_in.insert(END, str(X1 + radius))
            y2_value_in.insert(END, str(Y1 + radius))

    def draw_new_line(self, X, Y, A, B):
        try:
            self.screen_canvas.delete(self.line)
        except Exception:
            pass
        self.line = self.screen_canvas.create_line(
            X, Y, A, B, fill='red', width=4)
        return self.line
