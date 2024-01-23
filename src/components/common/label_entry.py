from tkinter import Label, Entry
from tkinter import CENTER, NS, EW


def label_entry(frame, label, column_arr, font, row, col, reg_entry):
    Label(frame, text=label, font=font, width=10).grid(
        row=row + 1, column=col, padx=10, pady=10, sticky=NS + EW
    )
    if len(column_arr) == 1:
        entry = Entry(
            frame,
            name=column_arr[0].lower(),
            font=font,
            justify=CENTER,
            validate="key",
            validatecommand=reg_entry,
        )
        entry.grid(row=row + 1, column=col + 1, padx=10, pady=10, sticky=NS + EW)
    else:
        entry = {}
        for j, val in enumerate(column_arr):
            Label(frame, text=val, font=font).grid(
                row=row, column=col + j + 1, padx=10, pady=10, sticky=NS + EW
            )
            entry[val] = Entry(
                frame,
                name=val.lower(),
                font=font,
                justify=CENTER,
                validate="key",
                validatecommand=reg_entry,
            )
            entry[val].grid(
                row=row + 1, column=col + j + 1, padx=10, pady=10, sticky=NS + EW
            )

    return entry
