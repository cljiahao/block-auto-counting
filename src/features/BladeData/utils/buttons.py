from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.BladeData import BladeData

from components.messagebox import CustomMessageBox
from features.BladeData.constants import blade_data_info
from utils.debug import error_handler


def _validate_blade_entry(
    parent: BladeData, blade_data: dict[str, str], key: str
) -> None:
    """Validates a blade data entry for emptiness and raises an error if invalid"""
    if blade_data[key] == "":
        CustomMessageBox(
            parent,
            blade_data_info[key]["error_title"],
            blade_data_info[key]["error_message"],
            "showerror",
        )
        raise ValueError(blade_data_info[key]["error_title"])


@error_handler()
def on_submit(parent: BladeData) -> None:
    """Processes, validate and saves blade data submitted from the BladeData component"""
    blade_data = {k: v.get() for k, v in parent.widgets["blade_input"].cache.items()}

    _validate_blade_entry(parent, blade_data, "blade_batch_no")
    _validate_blade_entry(parent, blade_data, "blade_life")

    parent.blade_data_service.create_or_update_blade_data(parent.lot_no, blade_data)

    parent.result = True
    parent.destroy()
