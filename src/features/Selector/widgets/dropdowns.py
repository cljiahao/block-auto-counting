from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.Selector import Selector

from tkinter import EW, NS
from tkinter import Frame

from constants.block import tape_defect_names
from components.ui.label_dropdown import LabelDropdown


class DropDownContainer(Frame):
    """
    Tkinter Frame holding labels and dropdown boxes for Selector component

    Args:
        parent: Selector Toplevel.
        dropdowns: List of strings to show in the dropdown box.
    """

    def __init__(self, parent: Selector, dropdowns: list[str]) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str, LabelDropdown] = {}
        self.default = "Choose 1"
        self.win_config(dropdowns)
        self.add_widgets(dropdowns)

    def win_config(self, dropdowns: list[str]) -> None:
        for i in range(len(dropdowns)):
            self.rowconfigure(i, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self, dropdowns: list[str]) -> None:
        for i, key in enumerate(dropdowns):
            self.widgets[key] = LabelDropdown(
                self,
                label=f"[{i+1}] {key.rsplit('_',1)[0]} :",
                value=self.default,
                option=tape_defect_names,
            )
            self.widgets[key].grid(
                row=i, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky=NS + EW
            )
