from tkinter import Frame, IntVar, Label, Checkbutton
from tkinter import NS, EW


def checkbox(frame, label, option, font, row, col):
    """Return Check Button component"""
    # Overall Label
    Label(frame, text=label, font=font, width=10).grid(
        row=row, column=col, padx=10, pady=10, sticky=NS + EW
    )

    # Frame to hold checkboxes
    check_frame = Frame(frame)
    check_frame.grid(row=row, column=col + 1)

    sel_var = {}
    for i in option:
        # Check Buttons with names beside it, 1 = True, 0 = False
        sel_var[i] = IntVar()
        drop_var = Checkbutton(
            check_frame, text=i, font=font, variable=sel_var[i], onvalue=1, offvalue=0
        )
        drop_var.grid(row=0, column=i, padx=10, pady=10, sticky=EW)

    return sel_var
