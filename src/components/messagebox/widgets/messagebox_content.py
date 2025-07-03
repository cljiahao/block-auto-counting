from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.messagebox import CustomMessageBox

from tkinter import EW, NS
from tkinter import Frame, Label

from constants.common import font_size
from core.directory_manager import directory_manager as dm
from utils.tkinter.tk_utils import TkinterImage


class CustomMessageBoxContent(Frame):
    """
    Tkinter Frame holding Labels to show info or error for CustomMessageBox component

    Args:
        parent: CustomMessageBox Toplevel.
        message: Message to show based on mode.
    """

    def __init__(self, parent: CustomMessageBox, message: str) -> None:
        super().__init__(parent)
        self.parent = parent
        self.logo = TkinterImage.resize_path_to_tkinter(
            dm.resource_path(f"assets/{parent.msgbox_mode['logo_name']}"),
            parent.win_size,
            0.5,
        )
        self.win_config()
        self.add_widgets(message)

    def win_config(self) -> None:
        self.config(bg=self.parent.msgbox_mode["bg"])
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=3, uniform="a")
        self.columnconfigure(1, weight=5, uniform="a")

    def add_widgets(self, message: str) -> None:
        Label(self, image=self.logo, bg=self.parent.msgbox_mode["bg"]).grid(
            row=0, column=0, padx=5, pady=5, sticky=NS + EW
        )
        Label(
            self,
            text=message,
            wraplength=self.parent.win_size["width"] / 2,
            bg=self.parent.msgbox_mode["bg"],
            font=font_size["xl"],
        ).grid(row=0, column=1, padx=5, pady=5, sticky=NS + EW)
