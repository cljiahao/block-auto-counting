from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Settings.widgets.config_tabs import ConfigTabs

from itertools import product
from tkinter import CENTER, EW, NS
from tkinter import Label, StringVar
from tkinter.ttk import Button, Entry, Frame

from pages.Settings.widgets.config_tabs.constants import chip_size_tab
from pages.Settings.widgets.config_tabs.utils.buttons import (
    reset_changes,
    save_chip_size,
)


class TabChipSize(Frame):
    """
    A Tkinter Frame that provides a user interface for configuring chip sizes.

    Args:
        parent: ConfigTabs Notebook
    """

    def __init__(self, parent: ConfigTabs):
        super().__init__(parent)
        self.parent = parent
        self.retrieve_db()
        self.cache: dict[str, StringVar] = {
            (key := "_".join(tuple_keys)): StringVar(
                value=self.database_map.get(key, "")
            )
            for tuple_keys in product(
                chip_size_tab["headers"], chip_size_tab["widgets"]
            )
        }
        self.win_config()
        self.add_widgets()

    def retrieve_db(self) -> None:
        self.database_map = (
            self.parent.parent.config_service.read_all_configurations_by_category(
                "chip_size"
            )
        )

    def win_config(self) -> None:
        self.rowconfigure(len(self.cache) + 1, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        for i in range(3):
            self.columnconfigure(i + 1, weight=2, uniform="a")

    def add_widgets(self) -> None:

        Button(self, text="Save Changes", command=lambda: save_chip_size(self)).grid(
            row=0, column=2, padx=5, pady=5, sticky=NS + EW
        )
        Button(self, text="Reset", command=lambda: reset_changes(self)).grid(
            row=0, column=3, padx=5, pady=5, sticky=NS + EW
        )

        for i, value in enumerate(chip_size_tab["headers"].values()):
            Label(self, text=value["name"], justify=CENTER).grid(
                row=1, column=i + 1, padx=5, pady=5, sticky=NS + EW
            )

        for j, (w_key, w_value) in enumerate(chip_size_tab["widgets"].items()):
            row = j + 2
            Label(self, text=w_value["name"]).grid(row=row, column=0, sticky=NS + EW)

            for k, h_key in enumerate(chip_size_tab["headers"]):
                Entry(self, textvariable=self.cache[f"{h_key}_{w_key}"]).grid(
                    row=row, column=k + 1, padx=5, pady=5, sticky=NS + EW
                )
