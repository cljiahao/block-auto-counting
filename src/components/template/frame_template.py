from tkinter import Frame, StringVar, Toplevel


class Template(Frame):
    def __init__(self, parent: Toplevel) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str,] = {}
        self.cache: dict[str, StringVar] = {}
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:
        pass
