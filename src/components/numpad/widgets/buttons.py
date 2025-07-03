from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.numpad import NumPad

from tkinter import EW, NS
from tkinter import Button, Frame

from constants.common import font_size
from components.numpad.utils.buttons import on_submit


class NumPadButton(Frame):
    """
    Tkinter Frame holding buttons for NumPad component

    Args:
        parent: CustomMessageBox Toplevel.
    """

    def __init__(self, parent: NumPad) -> None:
        super().__init__(parent)
        self.parent = parent
        self.win_config()
        self.add_widgets()

    def win_config(self):
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:
        Button(
            self,
            text="Submit",
            bg="PaleGreen1",
            font=font_size["m"],
            command=lambda: on_submit(self.parent),
        ).grid(row=0, column=0, ipadx=10, ipady=10, sticky=NS + EW)
