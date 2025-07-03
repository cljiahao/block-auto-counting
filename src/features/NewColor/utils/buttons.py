from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.NewColor import NewColor

from utils.debug import error_handler
from features.NewColor.constants import color_range_info


@error_handler()
def on_add_new(parent: NewColor) -> None:
    """Saves new color data to the database and closes the dialog"""
    color_entry = parent.widgets["color_entry"].widgets["label_entry"].entry.get()
    is_tape = parent.widgets["color_entry"].cache["check_button"].get()
    new_color_data = {
        "is_tape": is_tape,
        **{key: parent.color_range[key] for key in color_range_info},
    }

    result = parent.color_settings_service.create_or_update_color_specs(
        color_entry, new_color_data
    )
    parent.result = result.color
    parent.destroy()


@error_handler()
def on_cancel(parent: NewColor) -> None:
    """Closes the dialog without saving any changes"""
    parent.destroy()


buttons_map = {
    "add_new": on_add_new,
    "cancel": on_cancel,
}
