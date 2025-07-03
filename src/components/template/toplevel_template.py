from tkinter import StringVar, Toplevel

from utils.tkinter.tk_windows import window_size


class Template(Toplevel):
    def __init__(self, parent: Toplevel) -> None:
        super().__init__(parent)
        self.result = None
        self.widgets: dict[str,] = {}
        self.cache: dict[str, StringVar] = {}
        self.win_config()
        self.add_widgets()
        # To ensure window stays on top and focused
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def win_config(self) -> None:
        self.title("template")
        self.win_size = window_size(self)
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:
        pass
