from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Settings import Settings

from tkinter import EW, NS
from tkinter import LabelFrame

from pages.Settings.widgets.color_editor.widgets.buttons import SliderButtons
from pages.Settings.widgets.color_editor.widgets.sliders import Slider


class ColorEditor(LabelFrame):
    """
    Tkinter LabelFrame holding Color Slider and Buttons for Settings component

    Args:
        parent: Settings Toplevel.
    """

    def __init__(self, parent: Settings) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str, Slider | SliderButtons] = {}
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=5, uniform="a")
        self.rowconfigure(1, weight=3, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:

        self.widgets["slider"] = Slider(self)
        self.widgets["slider"].grid(row=0, column=0, padx=5, pady=5, sticky=NS + EW)

        self.widgets["slider_buttons"] = SliderButtons(self)
        self.widgets["slider_buttons"].grid(
            row=1, column=0, padx=5, pady=5, sticky=NS + EW
        )
