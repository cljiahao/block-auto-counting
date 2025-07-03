from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.AccuracyProfile import AccuracyProfile

from tkinter import EW, NS
from tkinter import Label, LabelFrame


class ColorLabel(LabelFrame):
    """
    Tkinter LabelFrame holding color name labels tied to changes for AccuracyProfile component

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
        for i in range(2):
            self.columnconfigure(i, weight=i + 1, uniform="a")

    def add_widgets(self) -> None:
        Label(self, text="Color").grid(
            row=0, column=0, padx=10, pady=10, sticky=NS + EW
        )

        Label(self, text=self.parent.color_name).grid(
            row=0, column=1, padx=10, pady=10, sticky=NS + EW
        )
