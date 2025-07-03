from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Settings import Settings

from tkinter.ttk import Notebook

from pages.Settings.widgets.config_tabs.widgets.tab_chip_size import TabChipSize
from pages.Settings.widgets.config_tabs.widgets.tab_settings import TabSettings


class ConfigTabs(Notebook):
    """
    A Notebook widget that manages configuration tabs for the for Settings component.

    Args:
        parent: Settings Toplevel
    """

    def __init__(self, parent: Settings) -> None:
        super().__init__(parent)
        self.parent = parent
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:
        tabs_settings = TabSettings(self)
        self.add(tabs_settings, text="Settings", padding=10)

        tabs_chip_size = TabChipSize(self)
        self.add(tabs_chip_size, text="Chip Size", padding=10)
