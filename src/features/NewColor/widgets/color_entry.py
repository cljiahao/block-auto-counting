from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.NewColor import NewColor

from tkinter import EW, N, NS, S
from tkinter import Checkbutton, IntVar, Label, LabelFrame

from components.ui.label_entry import LabelEntry


class ColorEntry(LabelFrame):
    """
    Tkinter LabelFrame holding color name entry and sticker checkbox for NewColor component

    Args:
        parent: NewColor Toplevel.
    """

    def __init__(self, parent: NewColor) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str, LabelEntry] = {}
        self.cache: dict[str, IntVar] = {"check_button": IntVar(value=0)}
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")
        self.columnconfigure(0, weight=3, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")

    def add_widgets(self) -> None:
        self.widgets["label_entry"] = LabelEntry(
            self, label="Color Name:", column_span=2
        )
        self.widgets["label_entry"].grid(
            row=0, column=0, rowspan=2, padx=5, pady=20, sticky=NS + EW
        )

        Label(self, text="Tape?").grid(row=0, column=1, padx=5, pady=3, sticky=S + EW)
        Checkbutton(
            self, variable=self.cache["check_button"], onvalue=1, offvalue=0
        ).grid(row=1, column=1, padx=5, pady=3, sticky=N + EW)
