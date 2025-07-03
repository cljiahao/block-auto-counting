from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Accuracy import Accuracy

from tkinter import EW, NS
from tkinter import Button, Frame

from constants.common import font_size
from pages.Accuracy.constants import buttons_info
from pages.Accuracy.utils.buttons import buttons_map


class AccuracyButton(Frame):
    """
    Tkinter Frame holding buttons for Accuracy component

    Args:
        parent: Accuracy Toplevel.
    """

    def __init__(self, parent: Accuracy) -> None:
        super().__init__(parent)
        self.parent = parent
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:
        for i, value in enumerate(buttons_info.values()):
            on_click = lambda value=value: buttons_map[value["button_key"]](self.parent)
            Button(
                self,
                text=value["name"],
                font=font_size[value["font"]],
                bg=value["bg"],
                fg=value["fg"],
                command=on_click,
            ).grid(
                row=0, column=1, ipadx=50, ipady=10, padx=30, pady=30, sticky=NS + EW
            )
