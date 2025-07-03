from tkinter import EW, NS, SUNKEN
from tkinter import Frame, Label, PhotoImage, Toplevel


class ImageHolder(Frame):
    """
    Tkinter Frame holding the label to insert image into.

    Args:
        parent: Toplevel to place the frame into.
    """

    def __init__(self, parent: Toplevel, image: PhotoImage = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str, Label] = {}
        self.win_config()
        self.add_widgets(image)

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self, image: PhotoImage) -> None:
        self.widgets["image"] = Label(self, relief=SUNKEN, image=image)
        self.widgets["image"].grid(
            row=0,
            column=0,
            sticky=NS + EW,
        )
