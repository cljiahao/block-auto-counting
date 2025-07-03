from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.Selector import Selector

from tkinter import EW, NS
from tkinter import Button, Frame

from constants.common import font_size
from features.Selector.constants import buttons_info
from features.Selector.utils.buttons import buttons_map


class SelectorButton(Frame):
    """
    Tkinter Frame holding buttons for Selector component

    Args:
        parent: Selector Toplevel.
    """

    def __init__(self, parent: Selector) -> None:
        super().__init__(parent)
        self.parent = parent
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        for i in range(len(buttons_info)):
            self.columnconfigure(i, weight=1, uniform="a")

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
                row=0, column=i, ipadx=50, ipady=10, padx=30, pady=30, sticky=NS + EW
            )
