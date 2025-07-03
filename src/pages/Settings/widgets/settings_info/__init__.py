from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Settings import Settings

from tkinter import EW, NS
from tkinter import LabelFrame

from components.ui.scroll_container import ScrollContainer
from pages.Settings.widgets.settings_info.widgets.color_material_defect import (
    ColorMaterialDefect,
)
from pages.Settings.widgets.settings_info.utils.tk_utils import (
    refresh_scroll_container,
)


class SettingsInfo(LabelFrame):
    """
    Tkinter LabelFrame holding scrollable container frame to hold settings info for Settings component.

    Args:
        parent: Settings Toplevel
    """

    def __init__(self, parent: Settings) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str, ScrollContainer, ColorMaterialDefect] = {}
        self.refresh_settings_info = lambda: refresh_scroll_container(self)
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:
        self.widgets["scroll_container"] = ScrollContainer(self)
        self.widgets["scroll_container"].grid(row=0, column=0, sticky=NS + EW)

        self.widgets["color_material_defect"] = ColorMaterialDefect(
            self.widgets["scroll_container"], self.parent.color_specs
        )
        self.widgets["color_material_defect"].grid(row=0, column=0, sticky=NS + EW)
