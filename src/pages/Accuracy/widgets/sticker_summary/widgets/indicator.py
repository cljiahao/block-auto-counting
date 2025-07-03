from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Accuracy.widgets.sticker_summary import StickerSummary

from tkinter import CENTER, DISABLED, EW, NS, RIDGE
from tkinter import Canvas, Entry, Frame, Label, StringVar


class Indicator(Frame):
    """
    Tkinter Frame holding labels and indicator to compare calculated and actual data StickerSummary component

    Args:
        parent: StickerSummary Toplevel.
        calc: Calculated data result to show.
        actual: Actual data result to show.
    """

    def __init__(self, parent: StickerSummary, calc: str, actual: str) -> None:
        super().__init__(parent)
        self.parent = parent
        self.win_size = parent.parent.win_size
        self.win_config()
        self.add_widgets(calc, actual)

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self, calc: str, actual: str) -> None:

        Label(
            self,
            text=calc,
            width=10,
            relief=RIDGE,
        ).grid(row=0, column=0, padx=5, pady=3, sticky=EW)

        Label(self, text="/").grid(row=0, column=1, padx=5, pady=3, sticky=NS + EW)

        Entry(
            self,
            textvariable=StringVar(value=actual),
            width=12,
            justify=CENTER,
            state=DISABLED,
        ).grid(row=0, column=2, padx=5, pady=3, sticky=EW)

        canvas = Canvas(
            self,
            width=int(1 / 40 * self.win_size["w_screen"]),
            height=int(1 / 24 * self.win_size["h_screen"]),
        )
        canvas.grid(row=0, column=3, padx=5, pady=3, sticky=NS + EW)
        canvas.create_oval(
            int(1 / 320 * self.win_size["w_screen"]),
            int(1 / 192 * self.win_size["h_screen"]),
            int(7 / 320 * self.win_size["w_screen"]),
            int(7 / 192 * self.win_size["h_screen"]),
        )
        canvas.addtag_withtag("circle", 1)

        # TODO: dynamic tolerance for pass_fail
        pass_fail = (
            "PaleGreen1"
            if abs(int(actual) - int(calc)) < int(actual) * 0.1
            else "salmon"
        )
        canvas.itemconfig("circle", fill=pass_fail)
