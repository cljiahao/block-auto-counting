from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Main import Main

from tkinter import RIDGE, W
from tkinter import Button, Frame, Label

from constants.block import defect_info
from pages.Main.utils.buttons import buttons_map


class DefectDetails(Frame):
    """
    Tkinter Frame holding defects information for Main component

    Args:
        parent: Main Toplevel.
    """

    def __init__(self, parent: Main) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str, Label] = {}
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        for i in range(len(defect_info) // 2):
            self.rowconfigure(i, weight=1)

    def add_widgets(self) -> None:
        for i, (key, defect) in enumerate(defect_info.items()):
            name = defect["name"]
            row = i // 2
            col = 0 if i % 2 == 0 else 3

            Label(self, text=f"[{key}]").grid(row=row, column=col, padx=3, pady=5)
            if defect["type"] == "button":
                on_click = lambda defect=defect, key=key, name=name: buttons_map[
                    defect["button_key"]
                ](self.parent, key, name)
                Button(self, text=f"{name}", command=on_click).grid(
                    row=row, column=col + 1, padx=3, pady=5, sticky=W
                )
            else:
                Label(self, text=f"{name}").grid(
                    row=row, column=col + 1, padx=3, pady=5, sticky=W
                )

            self.widgets[key] = Label(
                self,
                text=defect["value"],
                width=10,
                relief=RIDGE,
                bg="salmon" if defect["value"].lower() == "none" else "snow",
            )
            self.widgets[key].grid(row=row, column=col + 2, padx=3, pady=5)
