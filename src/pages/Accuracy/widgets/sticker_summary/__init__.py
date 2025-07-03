from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Accuracy import Accuracy

from tkinter import EW, NS, W
from tkinter import Frame, Label

from constants.common import font_size
from pages.Accuracy.widgets.sticker_summary.widgets.indicator import Indicator


class StickerSummary(Frame):
    """
    Tkinter Frame holding all processed data and actual data results comparison for Accuracy component

    Args:
        parent: Accuracy Toplevel.
        acc_result: list.
    """

    def __init__(self, parent: Accuracy, acc_result: list) -> None:
        super().__init__(parent)
        self.parent = parent
        self.acc_result = acc_result
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        for i in range(len(self.acc_result) + 1):
            self.rowconfigure(i, weight=1, uniform="a")

    def add_widgets(self) -> None:

        for i, header in enumerate(["Number of Stickers", "Total Area of Stickers"]):
            Label(self, text=header, font=font_size["s"]).grid(
                row=0, column=i + 1, sticky=NS + EW
            )

        for i, sticker in enumerate(self.acc_result):
            name = sticker["sticker_color"]
            Label(self, text=name, font=font_size["xs"]).grid(
                row=i + 1, column=0, padx=5, pady=3, sticky=NS + W
            )

            Indicator(self, sticker["sticker_count"], sticker["count"]).grid(
                row=i + 1, column=1, sticky=NS + EW
            )

            Indicator(self, sticker["sticker_area"], sticker["area"]).grid(
                row=i + 1, column=2, sticky=NS + EW
            )
