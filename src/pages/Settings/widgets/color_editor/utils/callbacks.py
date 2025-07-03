from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Settings.widgets.color_editor import ColorEditor

from tkinter import DISABLED, NORMAL
from tkinter.ttk import Combobox

from pages.Settings.widgets.color_editor.constants import slider_info


def combo_box(parent: ColorEditor) -> Combobox:
    return parent.widgets["slider_buttons"].widgets["material"].widgets["combo_box"]


def fetch(parent: ColorEditor, value: str) -> None:
    if not value:
        combo_box(parent)["state"] = DISABLED
        return

    color_specs = parent.parent.color_settings_service.read_color_specs_not_empty(value)
    low_keys = [key for key in slider_info if "low" in key]
    high_keys = [key for key in slider_info if "high" in key]

    hsv_values = {
        **dict(zip(low_keys, color_specs.lower_limit.split(","))),
        **dict(zip(high_keys, color_specs.upper_limit.split(","))),
    }
    for key, hsv_value in hsv_values.items():
        parent.widgets["slider"].cache[key].set(hsv_value)

    accuracy_profile = (
        parent.parent.color_settings_service.read_accuracy_profile_not_empty(value)
    )

    combo_box(parent)["values"] = [
        acc_profile.material
        for acc_profile in accuracy_profile
        if accuracy_profile[0] is not None
    ]
    combo_box(parent)["state"] = NORMAL
