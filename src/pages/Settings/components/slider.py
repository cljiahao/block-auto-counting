from tkinter import Label, Entry, IntVar
from tkinter import HORIZONTAL, CENTER, E, W
from tkinter import ttk


def slider(frame_slide, set_names):
    hsv_text = [
        "Low H: ",
        "High H: ",
        "Low S: ",
        "High S: ",
        "Low V: ",
        "High V: ",
    ]

    int_var = {}
    scale_hsv = {}
    entry_hsv = {}
    for i, txt in enumerate(hsv_text):
        # Algo for 0 or 255 on Scale / Slider
        limit = 0 if i % 2 == 0 else 255
        int_var[txt] = IntVar(value=limit)

        # HSV Low High Labels
        Label(frame_slide, text=txt, font=set_names["Font"]["M"]).grid(
            row=i + 1, column=0, padx=10, pady=(0, 5)
        )

        # HSV Entry Boxes
        entry_hsv[txt] = Entry(
            frame_slide,
            width=8,
            textvariable=str(int_var[txt]),
            font=set_names["Font"]["M"],
            justify=CENTER,
        )
        entry_hsv[txt].grid(row=i + 1, column=1, sticky=W)

        # Scale / Slider for adjusting HSV
        scale_hsv[txt] = ttk.Scale(
            frame_slide,
            variable=int_var[txt],
            from_=0,
            to=255,
            orient=HORIZONTAL,
            command=lambda event, txt=txt: int_var[txt].set(int(float(event))),
        )
        scale_hsv[txt].grid(
            row=i + 1, column=2, columnspan=3, padx=10, pady=(0, 5), sticky=E + W
        )

    return entry_hsv
