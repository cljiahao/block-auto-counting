from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Settings.widgets.color_editor import ColorEditor

from tkinter import EW, NS
from tkinter import Button, Frame

from constants.common import font_size
from components.ui.label_dropdown import LabelDropdown
from pages.Settings.widgets.color_editor.constants import buttons_info
from pages.Settings.widgets.color_editor.utils.buttons import buttons_map
from pages.Settings.widgets.color_editor.utils.callbacks import fetch


class SliderButtons(Frame):
    """
    Tkinter Frame holding buttons for ColorEditor component

    Args:
        parent: ColorEditor Toplevel.
    """

    def __init__(self, parent: ColorEditor) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str, LabelDropdown] = {}
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")
        for i in range(len(buttons_info)):
            self.columnconfigure(i, weight=1, uniform="a")

    def add_widgets(self) -> None:
        self.widgets["color_names"] = LabelDropdown(
            self,
            value="Select Color",
            option=self.parent.parent.color_names,
            callback=lambda value: fetch(self.parent, value),
            disabled=not self.parent.parent.color_names,
        )
        self.widgets["color_names"].grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky=NS + EW
        )

        self.widgets["material"] = LabelDropdown(
            self,
            value="Select Material",
            disabled=(
                self.widgets["color_names"].selection.get()
                == self.widgets["color_names"].default
            ),
        )
        self.widgets["material"].grid(
            row=0, column=2, columnspan=2, padx=5, pady=5, sticky=NS + EW
        )

        for i, (key, value) in enumerate(buttons_info.items()):
            on_click = lambda value=value: buttons_map[value["button_key"]](self.parent)
            self.widgets[key] = Button(
                self,
                text=value["name"],
                font=font_size[value["font"]],
                bg=value["bg"],
                fg=value["fg"],
                command=on_click,
            )
            self.widgets[key].grid(row=1, column=i, padx=5, pady=5, sticky=NS + EW)
