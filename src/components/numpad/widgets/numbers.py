from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.numpad import NumPad

from tkinter import EW, NS
from tkinter import Button, Frame

from constants.common import font_size


class Numbers(Frame):
    """
    Tkinter Frame holding number buttons for NumPad component

    Args:
        parent: CustomMessageBox Toplevel.
    """

    def __init__(self, parent: NumPad) -> None:
        super().__init__(parent)
        self.parent = parent
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        for i in range(4):
            self.rowconfigure(i, weight=1, uniform="a")
            if i == 3:
                continue
            self.columnconfigure(i, weight=1, uniform="a")

    def add_widgets(self) -> None:

        num_entry = self.parent.widgets["label_entry"].entry

        # Create "1" to "9" Buttons in a 3x3 matrix
        for i in range(9):
            row = i // 3
            col = i % 3
            Button(
                self,
                text=i + 1,
                font=font_size["s"],
                command=lambda pad=i + 1: num_entry.set(f"{num_entry.get()}{pad}"),
            ).grid(row=row, column=col, sticky=NS + EW)

        # Create "0" Button
        Button(
            self,
            text=0,
            font=font_size["s"],
            command=lambda: num_entry.set(f"{num_entry.get()}0"),
        ).grid(row=3, column=0, sticky=NS + EW)

        # Create "." Button
        Button(
            self,
            text=".",
            font=font_size["s"],
            command=lambda: num_entry.set(f"{num_entry.get()}."),
        ).grid(row=3, column=1, sticky=NS + EW)

        # Create "Del" Button
        Button(
            self,
            text="Del",
            font=font_size["s"],
            command=lambda: num_entry.set(num_entry.get()[:-1]),
        ).grid(row=3, column=2, sticky=NS + EW)
