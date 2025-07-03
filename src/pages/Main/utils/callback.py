from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Main.widgets.wos import WOSInfo

from db.session import get_db
from db.services.blade_data import BladeDataService
from services.prass import check_lot


def callback(parent: WOSInfo, prompt: str, name: str) -> bool:
    """Delegates entry matching based on the input field's name"""
    key_name = name.split(".")[-1]
    return entry_match(parent, prompt, key_name)


def entry_match(parent: WOSInfo, prompt: str, key_name: str) -> bool:
    """Matches entry input to specific handlers based on the field key"""
    prompt_length = len(prompt)

    match key_name:
        case "lot_no":
            return handle_lot_no_entry(parent, prompt, prompt_length)
        case "payroll_no":
            return handle_payroll_no_entry(parent, prompt, prompt_length)
        case "mc_no":
            return handle_mc_no_entry(parent, prompt, prompt_length)
    return True


def handle_lot_no_entry(parent: WOSInfo, prompt: str, prompt_length: int) -> bool:
    """Validates lot number entry, updates UI with lot info, and sets focus"""
    if prompt_length > 10:
        return False

    if prompt_length == 10:
        grandparent = parent.parent

        item, input_qty = check_lot(prompt)
        chip_code = ["Error!", "salmon"] if item == None else [item[:5], "PaleGreen1"]
        grandparent.widgets["wos_info"].widgets["chip_type"].config(
            text=chip_code[0], bg=chip_code[1]
        )

        db = next(get_db())
        blade_data_service = BladeDataService(db)
        blade_data_status = (
            ["PaleGreen1", "Added"]
            if blade_data_service.read_blade_data(prompt)
            else ["salmon", "None"]
        )
        parent.parent.widgets["defect_info"].widgets["BD"].config(
            bg=blade_data_status[0], text=blade_data_status[1]
        )

        grandparent.widgets["wos_info"].cache["input_qty"].set(input_qty)
        parent.widgets["payroll_no"].focus()

    return True


def handle_payroll_no_entry(parent: WOSInfo, prompt: str, prompt_length: int) -> bool:
    """Validates payroll number entry and sets focus to the next field"""
    if prompt_length > 7:
        return False

    if prompt_length == 7:
        parent.widgets["mc_no"].focus()

    return True


def handle_mc_no_entry(parent: WOSInfo, prompt: str, prompt_length: int) -> bool:
    """Validates machine number entry and sets focus to the input quantity"""
    if prompt_length > 3:
        return False

    if prompt_length == 3:
        parent.widgets["input_qty"].focus()

    return True
