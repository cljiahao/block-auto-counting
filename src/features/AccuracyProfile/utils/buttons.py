from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.AccuracyProfile import AccuracyProfile

from utils.debug import error_handler


def retrieve_accuracy_profile_entry(parent: AccuracyProfile) -> dict[str, str]:
    accuracy_entry = {
        key: value.get()
        for key, value in parent.widgets["accuracy_entry"].cache.items()
    }
    defect_mode = {
        "defect_mode": parent.widgets["profile_type"]
        .widgets["defect_mode"]
        .selection.get(),
    }
    return {**accuracy_entry, **defect_mode}


@error_handler()
def on_submit(parent: AccuracyProfile) -> None:
    """Retrieve entry added for accuracy profile and create into database with input"""
    material = parent.widgets["profile_type"].widgets["material"].selection.get()
    accuracy_profile = retrieve_accuracy_profile_entry(parent)
    parent.color_settings_service.create_or_update_accuracy_profile(
        parent.color_name, material, accuracy_profile
    )
    parent.result = material

    parent.destroy()


@error_handler()
def on_cancel(parent: AccuracyProfile) -> None:
    """Closes the dialog without saving any changes"""
    parent.destroy()


buttons_map = {
    "submit": on_submit,
    "cancel": on_cancel,
}
