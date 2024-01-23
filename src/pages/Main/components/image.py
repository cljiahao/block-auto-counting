from tkinter import Label
from tkinter import SUNKEN, NS, EW


def show_image(frame, set_names):
    # Display image on this container
    capture = Label(frame, relief=SUNKEN)
    capture.grid(
        row=0,
        column=0,
        rowspan=len(set_names["Defect Code"]) + 5,
        columnspan=2,
        padx=5,
        pady=10,
        sticky=NS + EW,
    )

    return capture
