from tkinter import Frame, Canvas, Scrollbar
from tkinter import VERTICAL, FLAT, NS, NW, EW


def scroll_cont(frame, canvas_size="8c"):
    # Frame for holding Canvas
    frame_canvas = Frame(frame, bd=5, relief=FLAT)
    frame_canvas.rowconfigure(0, weight=1)
    frame_canvas.columnconfigure(0, weight=1)
    frame_canvas.grid(row=0, column=0, sticky=NS + EW)

    # Canvas to create ScrollBar
    canvas = Canvas(frame_canvas, width=canvas_size)
    canvas.grid(row=0, column=0, sticky=NS + EW)

    # Scrollbar
    scroll = Scrollbar(frame_canvas, orient=VERTICAL, command=canvas.yview)
    scroll.grid(row=0, column=1, sticky=NS)

    canvas.config(yscrollcommand=scroll.set)
    canvas.bind(
        "<Configure>",
        lambda e: canvas.config(scrollregion=canvas.bbox("all")),
    )

    # Frame for inside Canvas
    inner_frame = Frame(canvas, bd=5, relief=FLAT)
    inner_frame.grid(row=0, column=0, sticky=NS + EW)

    canvas.create_window((0, 0), window=inner_frame, anchor=NW)

    return inner_frame
