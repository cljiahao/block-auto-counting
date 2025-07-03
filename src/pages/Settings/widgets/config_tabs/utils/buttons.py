from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Settings.widgets.config_tabs.widgets.tab_chip_size import (
        TabChipSize,
    )
    from pages.Settings.widgets.config_tabs.widgets.tab_settings import TabSettings

from components.messagebox import CustomMessageBox


def default_save_info(parent: TabChipSize | TabSettings) -> None:
    """Displays a info message box when save changes button is pressed"""
    CustomMessageBox(
        parent, "Saved Changes", "Data change saved or updated.", "showinfo"
    )


def reset_changes(parent: TabChipSize) -> None:
    """Resets the displayed chip size values to their last saved state from the database"""
    parent.retrieve_db()
    for key, value in parent.cache.items():
        value.set(parent.database_map[key] if key in parent.database_map else "")


def save_chip_size(parent: TabChipSize) -> None:
    """Saves the current chip size settings from the UI to the database"""
    chip_size_details = [
        {"key_name": key, "value": value.get()} for key, value in parent.cache.items()
    ]
    parent.parent.parent.config_service.bulk_create_or_update_configurations(
        "chip_size", chip_size_details
    )

    default_save_info(parent)


def save_settings(parent: TabSettings) -> None:
    """Saves the current general settings from the UI to the database"""
    settings_details = [
        {"key_name": key, "value": value.get()} for key, value in parent.cache.items()
    ]
    parent.parent.parent.config_service.bulk_create_or_update_configurations(
        "settings", settings_details
    )

    default_save_info(parent)
