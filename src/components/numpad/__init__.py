from tkinter import EW, NS
from tkinter import Toplevel

from components.numpad.widgets.buttons import NumPadButton
from components.numpad.widgets.numbers import Numbers
from components.ui.label_entry import LabelEntry
from constants.common import font_size
from utils.tkinter.tk_windows import window_size


class NumPad(Toplevel):
    """
    A custom Tkinter NumPad to input and return number values to a submit callback.

    Args:
        parent: The parent widget, usually Toplevel.
        mode: The mode that the num pad inputs is targeting to.
    """

    def __init__(self, parent: Toplevel, mode: str) -> None:
        super().__init__(parent)
        self.result = None
        self.widgets: dict[str, LabelEntry] = {}
        self.win_config()
        self.add_widgets(mode)
        # To ensure window stays on top and focused
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def win_config(self) -> None:
        self.title("Num Pad")
        self.win_size = window_size(self)
        self.win_size["width"] = int(self.win_size["w_screen"] * 0.25)
        self.win_size["height"] = int(self.win_size["h_screen"] * 0.6)
        x_position = int(self.win_size["w_screen"] / 4)
        y_position = int(self.win_size["h_screen"] / 10)
        self.geometry(
            f"{self.win_size['width']}x{self.win_size['height']}+{x_position}+{y_position}"
        )
        self.rowconfigure(1, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self, text: str) -> None:

        self.widgets["label_entry"] = LabelEntry(
            self,
            label=f"Input Quantity for {text}",
            font_size=font_size["l"],
            toColumn=True,
        )
        self.widgets["label_entry"].grid(
            row=0, column=0, padx=5, pady=5, sticky=NS + EW
        )

        Numbers(self).grid(row=1, column=0, sticky=NS + EW)

        NumPadButton(self).grid(row=2, column=0, sticky=NS + EW)
