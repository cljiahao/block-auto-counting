from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.ui.label_dropdown import LabelDropdown
    from pages.Settings.widgets.color_editor import ColorEditor
    from pages.Settings.widgets.color_editor.widgets.buttons import SliderButtons

from components.messagebox import CustomMessageBox
from features.NewColor import NewColor
from features.AccuracyProfile import AccuracyProfile
from pages.Settings.widgets.color_editor.constants import slider_info
from utils.tkinter.tk_windows import destroy_children


def default_warning(parent: ColorEditor) -> None:
    """Displays a warning message box when no option has been selected for an update operation"""
    CustomMessageBox(
        parent, "Missing Option", "Please select an option to update.", "showwarning"
    )


def slider_buttons(parent: ColorEditor) -> SliderButtons:
    """Retrieves the SliderButtons widget instance from the ColorEditor's widgets"""
    return parent.widgets["slider_buttons"]


def colors_dropdown(parent: ColorEditor) -> LabelDropdown:
    """Retrieves the color names LabelDropdown widget from the SliderButtons"""
    return slider_buttons(parent).widgets["color_names"]


def material_dropdown(parent: ColorEditor) -> LabelDropdown:
    """Retrieves the material LabelDropdown widget from the SliderButtons"""
    return slider_buttons(parent).widgets["material"]


def is_default_color(parent: ColorEditor) -> bool:
    """Checks if the currently selected color in the dropdown is the default color"""
    return colors_dropdown(parent).selection.get() == colors_dropdown(parent).default


def is_default_material(parent: ColorEditor) -> bool:
    """Checks if the currently selected material in the dropdown is the default material"""
    return (
        material_dropdown(parent).selection.get() == material_dropdown(parent).default
    )


def retrieve_hsv_colors(parent: ColorEditor) -> dict[str, str]:
    """Retrieves the current HSV color range values from the slider widgets"""
    lower_limit = []
    upper_limit = []
    for key, value in parent.widgets["slider"].cache.items():
        str_val = value.get()
        (lower_limit.append(str_val) if "low" in key else upper_limit.append(str_val))

    return {
        "lower_limit": ",".join(lower_limit),
        "upper_limit": ",".join(upper_limit),
    }


def refresh_slider_buttons(parent: ColorEditor, color: str) -> None:
    """Refreshes the slider buttons and updates the color dropdown selection"""
    parent.parent.retrieve_db()

    destroy_children(slider_buttons(parent))
    slider_buttons(parent).add_widgets()

    colors_dropdown(parent).selection.set(color)


def refresh_material_dropdown(parent: ColorEditor, color: str, material: str) -> None:
    """Refreshes the slider buttons and updates the material dropdown selection"""
    accuracy_profile = (
        parent.parent.color_settings_service.read_accuracy_profile_not_empty(color)
    )
    material_dropdown(parent).selection.set(material)
    material_dropdown(parent).widgets["combo_box"]["values"] = [
        acc_profile.material
        for acc_profile in accuracy_profile
        if accuracy_profile[0] is not None
    ]


def on_add_new(parent: ColorEditor) -> None:
    """Handles the "Add New" action for either a new color or a new material profile"""
    if is_default_color(parent):
        color_range = retrieve_hsv_colors(parent)
        color_entry = NewColor(parent, color_range).result
        if color_entry:
            refresh_slider_buttons(parent, color_entry)
    elif is_default_material(parent):
        selected_color = colors_dropdown(parent).selection.get()
        material = AccuracyProfile(parent, selected_color).result
        if material:
            refresh_material_dropdown(parent, selected_color, material)

    parent.parent.widgets["setting_info"].refresh_settings_info()


def on_update(parent: ColorEditor) -> None:
    """Handles the "Update" action for saving changes to color ranges or material profiles"""
    selected_color = colors_dropdown(parent).selection.get()
    if not is_default_material(parent):
        selected_material = material_dropdown(parent).selection.get()
        material = AccuracyProfile(parent, selected_color, selected_material).result
        if material:
            refresh_material_dropdown(parent, selected_color, material)
            parent.parent.widgets["setting_info"].refresh_settings_info()
    elif not is_default_color(parent):
        color_range = retrieve_hsv_colors(parent)
        parent.parent.color_settings_service.create_or_update_color_specs(
            selected_color, color_range
        )
        parent.parent.widgets["setting_info"].refresh_settings_info()
        CustomMessageBox(
            parent,
            "Color updated",
            f"Color range for {selected_color} is updated.",
            "showinfo",
        )
    else:
        default_warning(parent)


def on_reset(parent: ColorEditor) -> None:
    """Resets the HSV slider values to their default settings and refreshes the color dropdown"""
    for key, slider in slider_info.items():
        parent.widgets["slider"].cache[key].set(slider["value"])

    refresh_slider_buttons(parent, colors_dropdown(parent).default)


def on_remove(parent: ColorEditor) -> None:
    """Handles the "Remove" action for deleting a color or a material profile"""
    selected_color = colors_dropdown(parent).selection.get()
    selected_material = material_dropdown(parent).selection.get()
    additional_message = (
        "" if is_default_material(parent) else f" for {selected_material}"
    )

    if not is_default_color(parent):
        if CustomMessageBox(
            parent,
            "Confirm Remove?",
            f"Removing {selected_color}{additional_message}.",
            "askyesno",
        ).result:
            if is_default_material(parent):
                parent.parent.color_settings_service.delete_color_specs(selected_color)
            else:
                parent.parent.color_settings_service.delete_accuracy_profile(
                    selected_color, selected_material
                )
            refresh_slider_buttons(parent, colors_dropdown(parent).default)
            parent.parent.widgets["setting_info"].refresh_settings_info()
    else:
        default_warning(parent)


buttons_map = {
    "add_new": on_add_new,
    "update": on_update,
    "reset": on_reset,
    "remove": on_remove,
}
