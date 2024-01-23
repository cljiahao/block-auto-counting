from tkinter import Label
from tkinter import SUNKEN, NS, EW


def show_img_mask(frame_cam):
    # Display image on this container
    capture = Label(
        frame_cam,
        relief=SUNKEN,
    )
    capture.grid(row=0, column=0, sticky=NS + EW)

    return capture
