from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.Selector import Selector

from components.messagebox import CustomMessageBox
from features.Selector.widgets.dropdowns import DropDownContainer


def dropdown_container(parent: Selector) -> DropDownContainer:
    return parent.widgets["drop_down_cont"]


def validate_selections(parent: Selector) -> None:
    dropdowns = dropdown_container(parent).widgets
    for key in dropdowns:
        if dropdowns[key].selection.get() == dropdown_container(parent).default:
            error_message = "Selection not completed."
            CustomMessageBox(
                parent, "Please Select Defects.", error_message, "showerror"
            )
            raise ValueError(error_message)


def on_save_changes(parent: Selector) -> None:
    """Retrieves dropdown selections, save selections to result state, and closes window"""
    validate_selections(parent)

    dropdowns = dropdown_container(parent).widgets
    parent.result = {key: dropdowns[key].selection.get() for key in dropdowns}

    parent.destroy()


buttons_map = {
    "save_changes": on_save_changes,
}
