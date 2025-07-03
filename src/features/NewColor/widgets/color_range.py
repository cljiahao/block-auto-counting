from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.NewColor import NewColor

from tkinter import EW, NS
from tkinter import Label, LabelFrame

from components.ui.label_entry import LabelEntry
from features.NewColor.constants import color_range_info


class ColorRange(LabelFrame):
    """
    Tkinter LabelFrame holding HSV labels for NewColor component

    Args:
        parent: NewColor Toplevel.
    """

    def __init__(self, parent: NewColor) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str, LabelEntry] = {}
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        for i in range(2):
            self.rowconfigure(i, weight=1, uniform="a")
            self.columnconfigure(i, weight=1, uniform="a")
        self.columnconfigure(2, weight=1, uniform="a")

    def add_widgets(self) -> None:

        Label(self, text="HSV").grid(row=1, column=0, padx=10, pady=10, sticky=NS + EW)

        for i, (key, value) in enumerate(color_range_info.items()):
            Label(self, text=value["name"]).grid(
                row=0, column=i + 1, padx=5, pady=5, sticky=NS + EW
            )
            Label(self, text=self.parent.color_range[key]).grid(
                row=1, column=i + 1, padx=5, pady=5, sticky=NS + EW
            )
