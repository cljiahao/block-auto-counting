import os
import cv2
import copy
import random
from tkinter import (
    Toplevel,
    Frame,
)
from tkinter import (
    BOTH,
    FLAT,
    NS,
    EW,
)

from utils.directory import dire

from pages.Settings.components.buttons import save_buttons, slider_buttons
from pages.Settings.components.colors import color_container
from pages.Settings.components.image import show_img_mask
from pages.Settings.components.slider import slider
from pages.Settings.components.tabs_settings import tabs_settings
from pages.Main.utils.camera import camera
from pages.Settings.utils.image import filter_img
from utils.read_write import read_settings


class Settings(Toplevel):
    def __init__(self, mode, light, superuser):
        Toplevel.__init__(self)
        self.initialize(mode, light)
        self.win_config()
        self.widgets(superuser)
        self.grab_set()
        self.mainloop()

    def initialize(self, mode, light):
        self.res = False
        settings = read_settings()
        self.set_names = settings["Names"]
        self.set_colors = settings["Colors"]
        self.set_holder = copy.deepcopy(self.set_colors)
        self.set_set = settings["Settings"]
        self.cap = camera(settings)
        self.light = light
        self.troubleshoot = self.set_set["Troubleshoot"]
        if self.troubleshoot["Trouble"]:
            file_lists = [file for file in os.listdir(dire.path_trouble) if mode in file]
            file_name = (
                random.sample(file_lists, 1)[0]
                if self.troubleshoot["File Name"] == ""
                else self.troubleshoot["File Name"]
            )
            self.file_path = os.path.join(dire.path_trouble, file_name)
        else:
            self.light.light_switch(True)

    def show_frames(self):
        if self.troubleshoot["Trouble"]:
            frame = cv2.imread(self.file_path)
        else:
            _, frame = self.cap.read()
            frame = frame[
                :,
                int(int(self.set_set["Config"]["CamResWidth"]) / 6) : int(
                    int(self.set_set["Config"]["CamResWidth"]) / 6 * 5
                ),
            ]
        imgtk = filter_img(self, frame, self.entry_hsv)

        self.capture.imgtk = imgtk
        self.capture.config(image=imgtk)
        self.capture.after(10, self.show_frames)

    def win_config(self):
        self.title("Settings")
        self.state("zoomed")
        self.frame = Frame(self)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=2)
        self.frame.rowconfigure(3, weight=1)
        self.frame.columnconfigure(0, weight=2)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=5)
        self.frame.columnconfigure(3, weight=1)
        self.frame.columnconfigure(4, weight=1)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self, superuser):
        # FRAME: for creating container to display image
        frame_cam = Frame(
            self.frame,
            bd=5,
            relief=FLAT,
            highlightbackground="blue",
            highlightthickness=2,
        )
        frame_cam.rowconfigure(0, weight=1)
        frame_cam.columnconfigure(0, weight=1)
        frame_cam.grid(row=0, column=0, rowspan=4, sticky=NS + EW)

        self.capture = show_img_mask(frame_cam)

        # FRAME: for creating sliders
        frame_slide = Frame(
            self.frame,
            bd=5,
            relief=FLAT,
            highlightbackground="blue",
            highlightthickness=2,
        )
        frame_slide.columnconfigure(0, weight=1)
        frame_slide.columnconfigure(2, weight=9)
        frame_slide.grid(row=0, column=2, padx=10, sticky=NS + EW)

        self.entry_hsv = slider(frame_slide, self.set_names)

        # FRAME: (Scrollable) for showing colours
        frame_colors = Frame(
            self.frame,
            bd=5,
            relief=FLAT,
            highlightbackground="blue",
            highlightthickness=2,
        )
        frame_colors.rowconfigure(0, weight=1)
        frame_colors.columnconfigure(0, weight=1)
        frame_colors.grid(row=0, column=4, rowspan=3, padx=10, sticky=NS + EW)

        color_container(frame_colors, self)

        # FRAME: for Dropdown and Buttons to fetch, add and reset
        frame_drop_but = Frame(
            self.frame,
            bd=5,
            relief=FLAT,
            highlightbackground="blue",
            highlightthickness=2,
        )
        frame_drop_but.rowconfigure(0, weight=1)
        frame_drop_but.rowconfigure(1, weight=1)
        frame_drop_but.grid(row=1, column=2, padx=10, sticky=NS + EW)

        slider_buttons(
            frame_drop_but,
            self,
            frame_colors,
        )

        # FRAME: for tab container to edit settings
        frame_tab = Frame(
            self.frame,
            bd=5,
            relief=FLAT,
            highlightbackground="blue",
            highlightthickness=2,
        )
        frame_tab.rowconfigure(0, weight=1)
        frame_tab.columnconfigure(0, weight=1)
        frame_tab.grid(row=2, column=2, rowspan=2, padx=10, sticky=NS + EW)

        self.tab_boxes = tabs_settings(
            frame_tab, self.set_names, self.set_set, superuser
        )

        # FRAME: for Buttons to save or return
        frame_buttons = Frame(self.frame, bd=5, relief=FLAT)
        frame_buttons.rowconfigure(0, weight=1)
        frame_buttons.rowconfigure(1, weight=1)
        frame_buttons.columnconfigure(0, weight=1)
        frame_buttons.columnconfigure(1, weight=1)
        frame_buttons.grid(row=3, column=4, padx=10, sticky=NS + EW)

        save_buttons(self, frame_buttons)

        self.show_frames()
