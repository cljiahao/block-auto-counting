from tkinter import EW, NS, NW, VERTICAL
from tkinter import Canvas, Frame, Scrollbar, Toplevel


class ScrollContainer(Frame):
    """
    Tkinter Frame to establish a scrollable inner Frame. \n
    To use scrolling, place self.widgets["canvas_frame"] as parent to children.

    Args:
        parent: Toplevel to place the frame into.
    """

    def __init__(self, parent: Toplevel) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str, Frame] = {}
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:
        canvas = Canvas(self)
        canvas.grid(row=0, column=0, sticky=NS + EW)

        scrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky=NS)

        canvas.config(yscrollcommand=scrollbar.set)

        self.widgets["canvas_frame"] = Frame(canvas)
        self.widgets["canvas_frame"].columnconfigure(0, weight=1, uniform="a")
        self.widgets["canvas_frame"].bind(
            "<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all"))
        )

        canvas_window_id = canvas.create_window(
            (0, 0), window=self.widgets["canvas_frame"], anchor=NW
        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(canvas_window_id, width=canvas.winfo_width()),
        )
