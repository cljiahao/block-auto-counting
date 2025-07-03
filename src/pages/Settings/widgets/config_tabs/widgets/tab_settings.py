from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Settings.widgets.config_tabs import ConfigTabs

from tkinter import EW, LEFT, NS
from tkinter import Label, StringVar
from tkinter.ttk import Button, Entry, Frame, Radiobutton

from pages.Settings.widgets.config_tabs.constants import settings_tab
from pages.Settings.widgets.config_tabs.utils.buttons import (
    reset_changes,
    save_settings,
)


class TabSettings(Frame):
    """
    A Tkinter Frame that provides a user interface for configuring misc settings.

    Args:
        parent: ConfigTabs Notebook
    """

    def __init__(self, parent: ConfigTabs):
        super().__init__(parent)
        self.parent = parent
        self.retrieve_db()
        self.cache: dict[str, StringVar] = {
            key: StringVar(value=self.database_map.get(key, value.get("value", "")))
            for key, value in settings_tab["widgets"].items()
        }
        self.win_config()
        self.add_widgets()

    def retrieve_db(self) -> None:
        self.database_map = (
            self.parent.parent.config_service.read_all_configurations_by_category(
                "settings"
            )
        )

    def win_config(self) -> None:
        self.rowconfigure(len(self.cache) + 1, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        for i in range(2):
            self.columnconfigure(i + 1, weight=1, uniform="a")

    def add_widgets(self) -> None:

        Button(self, text="Save Changes", command=lambda: save_settings(self)).grid(
            row=0, column=1, padx=5, pady=5, sticky=NS + EW
        )
        Button(self, text="Reset", command=lambda: reset_changes(self)).grid(
            row=0, column=2, padx=5, pady=5, sticky=NS + EW
        )

        for j, (key, value) in enumerate(settings_tab["widgets"].items()):
            row = j + 1
            Label(self, text=value["name"], justify=LEFT).grid(
                row=row, column=0, sticky=NS + EW
            )
            if value["type"] == "entry":
                Entry(self, textvariable=self.cache[key]).grid(
                    row=row, column=1, columnspan=2, padx=5, pady=5, sticky=NS + EW
                )
            elif value["type"] == "radio":
                Radiobutton(
                    self, text="True", variable=self.cache[key], value="true"
                ).grid(row=row, column=1, padx=5, pady=5)
                Radiobutton(
                    self, text="False", variable=self.cache[key], value="false"
                ).grid(row=row, column=2, padx=5, pady=5)
