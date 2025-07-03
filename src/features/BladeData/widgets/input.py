from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.BladeData import BladeData

from tkinter import CENTER, EW, NS, W
from tkinter import Entry, Frame, Label, OptionMenu, StringVar

from constants.common import font_size
from features.BladeData.constants import blade_data_info


class BladeInput(Frame):
    """
    Tkinter Frame holding inputs and labels for BladeData component

    Args:
        parent: BladeData Toplevel.
    """

    def __init__(self, parent: BladeData) -> None:
        super().__init__(parent)
        self.parent = parent
        stored_data = parent.blade_data_service.read_blade_data(parent.lot_no)
        self.cache: dict[str, StringVar] = {
            key: StringVar(
                value=(
                    getattr(stored_data, key)
                    if stored_data
                    else (
                        value[0] if isinstance(value := blade["value"], list) else value
                    )
                )
            )
            for key, blade in blade_data_info.items()
        }
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")

    def add_widgets(self) -> None:
        for i, (key, blade) in enumerate(blade_data_info.items()):

            Label(self, text=blade["name"], font=font_size["m"], justify=CENTER).grid(
                row=i, column=0, padx=10, pady=10, sticky=W
            )

            if isinstance(blade["value"], list):
                option_menu = OptionMenu(self, self.cache[key], *blade["value"])
                option_menu.config(font=font_size["m"])
                option_menu["menu"].config(font=font_size["m"])
                option_menu.grid(row=i, column=1, padx=10, pady=10, sticky=NS + EW)
            else:
                Entry(
                    self,
                    name=key.lower(),
                    textvariable=self.cache[key],
                    font=font_size["s"],
                    justify=CENTER,
                ).grid(row=i, column=1, padx=10, pady=10, sticky=NS + EW)
