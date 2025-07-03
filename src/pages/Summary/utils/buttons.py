from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.Summary import Summary

from components.messagebox import CustomMessageBox
from constants.block import defect_info
from core.directory_manager import directory_manager as dm
from core.file_manager import FileManager
from datetime import datetime as dt

from features.BladeData import BladeData
from services.prass import send_prass_file_server
from utils.tkinter.tk_windows import destroy_children


def on_delete(parent: Summary, index: int):
    """Delete existing defects data and refresh data"""
    defects_data_id = parent.lot_data.defects_data[index].id
    parent.lot_data_service.delete_defects_data(defects_data_id)

    parent.retrieve_db()

    destroy_children(parent.widgets["defect_summary"])
    parent.widgets["defect_summary"].add_widgets()


def on_blade_data(parent: Summary):
    if BladeData(parent, parent.lot_no).result:
        pass
        # TODO: update to green if blade data updated
        # defect_labels_widgets(parent, key).config(bg="PaleGreen1", text="Added")


def on_container_info(parent: Summary):
    pass


def on_submit(parent: Summary):
    date = dt.now().strftime("%Y/%m/%d")
    time = dt.now().strftime("%H:%M:%S")

    defects_string = ""
    total = 0
    for key in defect_info:
        sum_defects = sum(int(x) for x in parent.defects_dict[key])
        if 0 < sum_defects:
            defects_string += f"{key}|{sum_defects}"
        total += sum_defects

    prass_data = (
        f"{parent.lot_no}|{parent.mc_no}|{parent.payroll_no}|{date}|{time}|"
        f"{parent.input_qty}|{int(parent.input_qty) - total}|{defects_string}"
    )

    # Range predetermined (Can be changed to increase [Currently 26])
    delimiter_count = prass_data.count("|")
    for _ in range(26 - delimiter_count):
        prass_data += "|"

    current_month_prass_dir = dm.prass_dir / dt.today().strftime("%b%y")
    dm.create_directory(current_month_prass_dir)

    txt_file_path = current_month_prass_dir / f"{parent.lot_no}.txt"
    FileManager.write_txt(txt_file_path, prass_data)

    try:
        send_prass_file_server(txt_file_path)
    except Exception as e:
        CustomMessageBox(parent, "Sending to PRASS Error", str(e), "showerror")

    parent.result = True
    parent.destroy()


def on_cancel(parent: Summary):
    """Closes window upon button click"""
    parent.destroy()


buttons_map = {
    "blade_data": on_blade_data,
    "container_info": on_container_info,
    "submit": on_submit,
    "cancel": on_cancel,
}
