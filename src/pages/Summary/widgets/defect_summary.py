from __future__ import annotations
from typing import TYPE_CHECKING

from pages.Summary.utils.buttons import on_delete

if TYPE_CHECKING:
    from pages.Summary import Summary

from tkinter import EW, NS, W, Button
from tkinter import Frame, Label

from constants.block import defect_info


class DefectSummary(Frame):
    """
    Tkinter Frame holding defect info labels and saved data for Summary component

    Args:
        parent: Summary Toplevel.
    """

    def __init__(self, parent: Summary) -> None:
        super().__init__(parent)
        self.parent = parent
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        for i in range(len(defect_info) + 2):
            self.rowconfigure(i, weight=1, uniform="a")

    def add_widgets(self) -> None:
        Label(self, text="Block Numbers:").grid(
            row=0, column=0, columnspan=2, padx=3, pady=2, sticky=NS + EW
        )
        for a in range(len(self.parent.lot_data.defects_data)):
            Label(self, text=f"Block {a+1}").grid(
                row=0, column=a + 2, padx=5, pady=2, sticky=NS + EW
            )
            Button(
                self,
                text="x",
                bg="salmon",
                command=lambda index=a: on_delete(self.parent, index),
            ).grid(row=len(defect_info) + 1, column=a + 2)

        for i, (key, value) in enumerate(defect_info.items()):
            if key == "BD":
                continue
            Label(self, text=f"{value['name']}").grid(
                row=i + 1, column=0, padx=5, pady=2, sticky=NS + W
            )
            Label(self, text=key).grid(
                row=i + 1, column=1, padx=5, pady=2, sticky=NS + EW
            )

            for j, defect_value in enumerate(self.parent.defects_dict[key]):
                Label(self, text=defect_value).grid(
                    row=i + 1, column=j + 2, padx=5, pady=2, sticky=NS + EW
                )
