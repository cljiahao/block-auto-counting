from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Settings.widgets.color_editor import ColorEditor

from tkinter import CENTER, EW, HORIZONTAL, W
from tkinter import Entry, Frame, Label, StringVar
from tkinter.ttk import Scale

from pages.Settings.widgets.color_editor.constants import slider_info


class Slider(Frame):
    """
    Tkinter Frame holding sliders (low and high HSV) for ColorEditor component

    Args:
        parent: ColorEditor Toplevel.
    """

    def __init__(self, parent: ColorEditor) -> None:
        super().__init__(parent)
        self.cache: dict[str, StringVar] = {
            key: StringVar(value=slider["value"]) for key, slider in slider_info.items()
        }
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        for i in range(len(slider_info)):
            self.rowconfigure(i, weight=1, uniform="a")
        self.columnconfigure(2, weight=1, uniform="a")

    def add_widgets(self) -> None:
        for i, (key, slider) in enumerate(slider_info.items()):

            Label(self, text=f"{slider['name']}:").grid(
                row=i, column=0, padx=10, pady=3, sticky=W
            )

            Entry(
                self, width=8, textvariable=str(self.cache[key]), justify=CENTER
            ).grid(row=i, column=1, sticky=W)

            Scale(
                self,
                variable=self.cache[key],
                from_=0,
                to=255,
                orient=HORIZONTAL,
                command=lambda event, key=key: self.cache[key].set(int(float(event))),
            ).grid(row=i, column=2, columnspan=3, padx=10, pady=(0, 5), sticky=EW)
