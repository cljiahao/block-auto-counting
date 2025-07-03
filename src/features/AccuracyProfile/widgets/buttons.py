from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.AccuracyProfile import AccuracyProfile

from tkinter import EW, NS
from tkinter import Button, Frame

from constants.common import font_size
from features.AccuracyProfile.constants import buttons_info
from features.AccuracyProfile.utils.buttons import buttons_map


class EditAccuracyButtons(Frame):
    """
    Tkinter Frame holding buttons for AccuracyProfile component

    Args:
        parent: AccuracyProfile Toplevel.
    """

    def __init__(self, parent: AccuracyProfile) -> None:
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
                row=1,
                column=i,
                padx=5,
                pady=5,
                ipadx=3,
                ipady=3,
                sticky=NS + EW,
            )
