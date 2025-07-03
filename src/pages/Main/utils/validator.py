from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Main import Main

from components.messagebox import CustomMessageBox
from pages.Main.constants import wos_info


def validate_full_wos(parent: Main) -> None:
    """Validate wrapper for the entirety of wos information"""
    validate_full_entry(parent)
    validate_chip_size(parent)
    validate_material_selection(parent)


def validate_full_entry(parent: Main) -> None:
    """Validate wrapper for the entries of wos information"""
    validate_lot_no_entry(parent)
    validate_payroll_no_entry(parent)
    validate_mc_no_entry(parent)
    validate_input_qty_entry(parent)


def validate_lot_no_entry(parent: Main) -> None:
    """Validates the length of the lot number entry, raising ValueError if invalid"""
    lot_no_key = "lot_no"
    lot_no = parent.widgets["wos_info"].cache[lot_no_key].get()
    if len(lot_no) != 10:
        CustomMessageBox(
            parent,
            wos_info[lot_no_key]["error_title"],
            wos_info[lot_no_key]["error_message"],
            "showerror",
        )
        raise ValueError(wos_info[lot_no_key]["error_title"])


def validate_payroll_no_entry(parent: Main) -> None:
    """Validates the length of the payroll number entry, raising ValueError if invalid"""
    payroll_no_key = "payroll_no"
    payroll_no = parent.widgets["wos_info"].cache[payroll_no_key].get()
    if len(payroll_no) != 7:
        CustomMessageBox(
            parent,
            wos_info[payroll_no_key]["error_title"],
            wos_info[payroll_no_key]["error_message"],
            "showerror",
        )
        raise ValueError(wos_info[payroll_no_key]["error_title"])


def validate_mc_no_entry(parent: Main) -> None:
    """Validates the length of the machine number entry, raising ValueError if invalid"""
    mc_no_key = "mc_no"
    mc_no = parent.widgets["wos_info"].cache[mc_no_key].get()
    if len(mc_no) != 3:
        CustomMessageBox(
            parent,
            wos_info[mc_no_key]["error_title"],
            wos_info[mc_no_key]["error_message"],
            "showerror",
        )
        raise ValueError(wos_info[mc_no_key]["error_title"])


def validate_input_qty_entry(parent: Main) -> None:
    """Validates that the input quantity entry is not empty, raising ValueError if so"""
    input_qty_key = "input_qty"
    input_qty = parent.widgets["wos_info"].cache[input_qty_key].get()
    if not len(input_qty):
        CustomMessageBox(
            parent,
            wos_info[input_qty_key]["error_title"],
            wos_info[input_qty_key]["error_message"],
            "showerror",
        )
        raise ValueError(wos_info[input_qty_key]["error_title"])


def validate_chip_size(parent: Main) -> None:
    chip_size = parent.widgets["wos_info"].widgets["chip_type"].cget("text")[-2:]
    if not any(chip_size in key for key in parent.chip_size_data):
        error_message = f"Chip Size or Type : {chip_size} not found in database."
        CustomMessageBox(
            parent,
            "Chip Size not found",
            error_message,
            "showerror",
        )
        raise ValueError(error_message)


def validate_material_selection(parent: Main) -> None:
    material = parent.widgets["wos_info"].widgets["material"].selection.get()
    if material not in parent.unique_materials:
        error_message = f"Material Type : {material} not found in database."
        CustomMessageBox(
            parent,
            "Material Type not found",
            error_message,
            "showerror",
        )
        raise ValueError(error_message)
