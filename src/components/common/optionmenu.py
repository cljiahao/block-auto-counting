from tkinter import Label, StringVar, OptionMenu
from tkinter import NS, EW


def dropdown(frame, label, initial, option, font, menufont, row, col):
    """Return OptionMenu with Label component"""
    # Label for DropDown Box
    Label(frame, text=label, font=font, width=10).grid(
        row=row, column=col, padx=10, pady=10, sticky=NS + EW
    )

    # OptionMenu with options included while showing initial
    sel_var = StringVar(value=initial)
    drop_var = OptionMenu(frame, sel_var, *option)
    drop_var.config(font=font)
    drop_var["menu"].config(font=menufont)
    drop_var.grid(row=row, column=col + 1, padx=10, pady=10, sticky=EW)

    return sel_var
