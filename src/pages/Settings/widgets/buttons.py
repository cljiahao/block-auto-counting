from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Settings import Settings

from tkinter import Button, Frame, StringVar

from constants.common import font_size
from pages.Settings.constants import buttons_info
from pages.Settings.utils.buttons import buttons_map


class SettingsButton(Frame):
    """
    Tkinter Frame holding buttons for Settings component

    Args:
        parent: Settings Toplevel.
    """

    def __init__(self, parent: Settings) -> None:
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
        for i, value in enumerate(buttons_info.values()):
            on_click = lambda value=value: buttons_map[value["button_key"]](self.parent)
            Button(
                self,
                text=value["name"],
                font=font_size[value["font"]],
                bg=value["bg"],
                fg=value["fg"],
                command=on_click,
            ).grid(row=0, column=i, padx=5, pady=5, ipadx=20, ipady=10)
