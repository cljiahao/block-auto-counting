from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Summary import Summary


from constants.common import font_size
from pages.Summary.constants import buttons_info
from pages.Summary.utils.buttons import buttons_map
from tkinter import Button, Frame, StringVar


class SummaryButtons(Frame):
    """
    Tkinter Frame holding buttons for Summary component

    Args:
        parent: Summary Toplevel.
    """

    def __init__(self, parent: Summary) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str,] = {}
        self.cache: dict[str, StringVar] = {}
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
            ).grid(row=0, column=i, padx=5, pady=5, ipadx=20, ipady=5)
