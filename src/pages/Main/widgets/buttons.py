from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Main import Main

from tkinter import EW, NS
from tkinter import Button, Frame

from constants.common import font_size
from pages.Main.constants import buttons_info
from pages.Main.utils.buttons import buttons_map


class MainButtons(Frame):
    """
    Tkinter Frame holding buttons for Main component

    Args:
        parent: Main Toplevel.
    """

    def __init__(self, parent: Main) -> None:
        super().__init__(parent)
        self.parent = parent
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        for i in range(3):
            self.columnconfigure(i, weight=1)

    def add_widgets(self) -> None:
        for i, value in enumerate(buttons_info.values()):
            on_click = lambda value=value: buttons_map[value["button_key"]](self.parent)
            button = Button(
                self,
                text=value["name"],
                font=font_size[value["font"]],
                bg=value["bg"],
                fg=value["fg"],
                command=on_click,
            )
            button.grid(
                row=i // 3,
                column=i % 3,
                columnspan=1 if i // 3 == 0 else 3,
                padx=5,
                pady=3,
                ipadx=3,
                ipady=3,
                sticky=NS + EW,
            )
