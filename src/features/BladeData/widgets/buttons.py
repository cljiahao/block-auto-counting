from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.BladeData import BladeData

from tkinter import EW, NS
from tkinter import Button, Frame

from constants.common import font_size
from features.BladeData.utils.buttons import on_submit


class BladeButton(Frame):
    """
    Tkinter Frame holding buttons for BladeData component

    Args:
        parent: BladeData Toplevel.
    """

    def __init__(self, parent: BladeData) -> None:
        super().__init__(parent)
        self.parent = parent
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:
        Button(
            self,
            text="Submit",
            font=font_size["m"],
            bg="PaleGreen1",
            command=lambda: on_submit(self.parent),
        ).grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky=NS + EW)
