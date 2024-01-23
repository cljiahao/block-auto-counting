from tkinter import OptionMenu, Button, StringVar
from tkinter import ACTIVE, DISABLED, EW

from pages.Settings.utils.buttons import button_diff, no_change, save, staticnames


def slider_buttons(frame_drop_but, root, frame_colors):
    # Drop down box to select colour
    sel_col = StringVar(value="Select Colour:")
    drop_col = OptionMenu(
        frame_drop_but,
        sel_col,
        *root.set_colors,
        command=lambda event: drop_mat.config(state=ACTIVE),
    )
    drop_col.grid(row=0, column=0, columnspan=2, padx=15, ipadx=10, ipady=5, sticky=EW)

    # Drop down box to select material
    sel_mat = StringVar(value="Select Material:")
    drop_mat = OptionMenu(frame_drop_but, sel_mat, *root.set_set["Accuracy"])
    drop_mat.config(state=DISABLED)
    drop_mat.grid(row=0, column=2, columnspan=2, padx=15, ipadx=10, ipady=5, sticky=EW)

    # Button for Fetching, Adding and Reseting color data
    button_names = ["Fetch", "Add", "Reset", "New"]
    for i, name in enumerate(button_names):
        frame_drop_but.columnconfigure(i, weight=1)
        Button(
            frame_drop_but,
            text=name,
            command=lambda name=name: button_diff(
                root,
                name,
                sel_col.get(),
                sel_mat.get(),
                frame_drop_but,
                frame_colors,
            ),
        ).grid(row=1, column=i, padx=15, ipadx=10, ipady=5, sticky=EW)


def save_buttons(root, frame_buttons):
    Button(
        frame_buttons,
        text="Static Names",
        state=DISABLED,
        command=lambda: staticnames(root),
    ).grid(row=0, column=0, columnspan=2, padx=10, ipadx=10, ipady=5, sticky=EW)

    Button(frame_buttons, text="Save Changes", command=lambda: save(root)).grid(
        row=1, column=0, padx=10, ipadx=10, ipady=5, sticky=EW
    )

    Button(frame_buttons, text="No Changes", command=lambda: no_change(root)).grid(
        row=1, column=1, padx=10, ipadx=10, ipady=5, sticky=EW
    )
