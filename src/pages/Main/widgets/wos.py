from __future__ import annotations
from typing import TYPE_CHECKING

from components.ui.label_dropdown import LabelDropdown

if TYPE_CHECKING:
    from pages.Main import Main

from tkinter import CENTER, EW, LEFT, NS, W
from tkinter import Entry, Frame, Label, StringVar

from constants.common import font_size
from pages.Main.constants import wos_info
from pages.Main.utils.callback import callback


class WOSInfo(Frame):
    """
    Tkinter Frame holding WOS entry and information from PRASS for Main component

    Args:
        parent: Main Toplevel.
    """

    def __init__(self, parent: Main) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str, Entry | Label | LabelDropdown] = {}
        self.cache: dict[str, StringVar] = {
            key: StringVar(value=wos["value"]) for key, wos in wos_info.items()
        }
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, weight=1)
        self.reg_entry = (
            self.register(lambda input, name: callback(self, input, name)),
            "%P",
            "%W",
        )

    def add_widgets(self) -> None:
        for i, (key, wos) in enumerate(wos_info.items()):
            row = i // 2
            col = 0 if i % 2 == 0 else 2

            Label(self, text=wos["name"], wraplength=50, justify=LEFT).grid(
                row=row, column=col, padx=3, pady=5, sticky=W
            )

            self.widgets[key] = Entry(
                self,
                name=key.lower(),
                textvariable=self.cache[key],
                font=font_size["s"],
                width=10,
                justify=CENTER,
                validate="key",
                validatecommand=self.reg_entry,
            )
            self.widgets[key].grid(
                row=row, column=col + 1, padx=3, pady=5, sticky=NS + EW
            )

        type_row = len(wos_info) // 2 + 1

        self.widgets["chip_type"] = Label(
            self, text="Chip Type", font=font_size["m"], bg="light goldenrod"
        )
        self.widgets["chip_type"].grid(
            row=type_row, column=0, columnspan=2, padx=3, pady=5, sticky=NS + EW
        )

        # TODO: retrieve material type from prass url?
        self.widgets["material"] = LabelDropdown(
            self,
            value=next(iter(self.parent.unique_materials), "No material found"),
            option=self.parent.unique_materials,
        )
        self.widgets["material"].grid(
            row=type_row, column=2, columnspan=2, padx=3, pady=5, sticky=NS + EW
        )
