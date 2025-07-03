from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.ui.scroll_container import ScrollContainer

from tkinter import E, EW, NS, W
from tkinter import Label, Frame

from constants.common import font_size
from db.models.color_specs import ColorSpecs


class ColorMaterialDefect(Frame):
    """
    Tkinter Frame holding labels for saved color, material and defect mode data for Settings component

    Args:
        parent: Settings Toplevel.
    """

    def __init__(self, parent: ScrollContainer, color_specs: list[ColorSpecs]) -> None:
        canvas_frame = parent.widgets["canvas_frame"]
        super().__init__(canvas_frame)
        self.color_specs = color_specs
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")
        self.columnconfigure(2, weight=2, uniform="a")

    def add_widgets(self) -> None:

        Label(self, text="Color").grid(row=0, column=0, padx=5, pady=5, sticky=NS + W)
        Label(self, text="Material").grid(
            row=0, column=1, padx=5, pady=5, sticky=NS + E
        )
        Label(self, text="Defect Mode").grid(
            row=0, column=2, padx=5, pady=5, sticky=NS + EW
        )

        i = 1
        for color_spec in self.color_specs:
            Label(
                self, text=color_spec.color, font=(*font_size["default"], "bold")
            ).grid(row=i, column=0, columnspan=2, padx=5, pady=3, sticky=NS + W)
            i += 1
            if not color_spec.accuracy_profile:
                Label(self, text="Missing Mat & Defect", bg="salmon").grid(
                    row=i, column=1, columnspan=2, padx=5, pady=3, sticky=NS + EW
                )
                i += 1
            for acc_profile in color_spec.accuracy_profile:
                Label(self, text=acc_profile.material).grid(
                    row=i, column=1, padx=5, pady=3, sticky=NS + E
                )
                Label(self, text=acc_profile.defect_mode).grid(
                    row=i, column=2, padx=5, pady=3, sticky=NS + EW
                )
                i += 1
