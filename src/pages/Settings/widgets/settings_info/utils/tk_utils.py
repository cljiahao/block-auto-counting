from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Settings.widgets.settings_info import SettingsInfo

from utils.tkinter.tk_windows import destroy_children


def refresh_scroll_container(parent: SettingsInfo) -> None:
    """Re-render the container with information added or updated"""
    parent.parent.retrieve_db()

    destroy_children(parent)
    parent.add_widgets()
