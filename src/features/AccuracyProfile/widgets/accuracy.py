from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.AccuracyProfile import AccuracyProfile

from tkinter import EW, NS
from tkinter import Entry, Label, LabelFrame, StringVar

from features.AccuracyProfile.constants import accuracy_info


class AccuracyEntry(LabelFrame):
    """
    Tkinter LabelFrame holding AccuracyEntry (sticker count, sticker area) inputs and labels for AccuracyProfile component

    Args:
        parent: AccuracyProfile Toplevel.
    """

    def __init__(self, parent: AccuracyProfile) -> None:
        super().__init__(parent)
        self.cache: dict[str, StringVar] = {
            key: StringVar(
                value=(
                    getattr(parent.accuracy_profile[0], key, "")
                    if parent.material and len(parent.accuracy_profile) == 1
                    else value["value"]
                )
            )
            for key, value in accuracy_info.items()
        }
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")
        for i in range(3):
            self.columnconfigure(i, weight=2, uniform="a")

    def add_widgets(self) -> None:
        Label(self, text="Stickers").grid(
            row=1, column=0, padx=10, pady=10, sticky=NS + EW
        )

        for i, (key, value) in enumerate(accuracy_info.items()):
            Label(self, text=value["name"]).grid(
                row=0, column=i + 1, padx=10, pady=10, sticky=NS + EW
            )

            Entry(self, textvariable=self.cache[key]).grid(
                row=1, column=i + 1, padx=10, pady=10, sticky=NS + EW
            )
