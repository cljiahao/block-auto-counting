from __future__ import annotations
from typing import TYPE_CHECKING

from components.messagebox import CustomMessageBox

if TYPE_CHECKING:
    from pages.Main import Main

import cv2
import math
import random
import numpy as np
from collections import defaultdict
from datetime import datetime as dt
from tkinter import Entry, Label

from constants.block import reverse_defect_mapping
from constants.colors import BGRColors
from components.numpad import NumPad
from core.directory_manager import directory_manager as dm
from features.BladeData import BladeData
from features.Selector import Selector
from pages.Accuracy import Accuracy
from pages.Main.utils.validator import (
    validate_full_entry,
    validate_full_wos,
    validate_lot_no_entry,
    validate_material_selection,
)
from pages.Main.utils.process_defects import process_defects
from pages.Settings import Settings
from pages.Summary import Summary
from schemas.defects import DefectsInfoList, NPColorSpec
from utils.debug import error_handler
from utils.image_process.blob_handler import BlobHandler
from utils.image_process.image_manager import ImageManager
from utils.tkinter.tk_utils import TkinterImage


def image_holder_widgets(parent: Main) -> Label:
    return parent.widgets["image_holder"].widgets["image"]


def defect_labels_widgets(parent: Main, key) -> Entry | Label:
    return parent.widgets["defect_info"].widgets[key]


def wos_lot_no_value(parent: Main) -> str:
    return parent.widgets["wos_info"].cache["lot_no"].get()


def wos_payroll_no_value(parent: Main) -> str:
    return parent.widgets["wos_info"].cache["payroll_no"].get()


def wos_mc_no_value(parent: Main) -> str:
    return parent.widgets["wos_info"].cache["mc_no"].get()


def wos_input_qty_value(parent: Main) -> str:
    return parent.widgets["wos_info"].cache["input_qty"].get()


def get_chip_area(parent: Main) -> str:
    chip_type = parent.widgets["wos_info"].widgets["chip_type"].cget("text")[-2:]
    chip_length = float(parent.chip_size_data[f"length_{chip_type}"])
    chip_width = float(parent.chip_size_data[f"width_{chip_type}"])
    return chip_length * chip_width


def material_type_selection(parent: Main) -> str:
    return parent.widgets["wos_info"].widgets["material"].selection.get()


def accuracy_profile_lookup(parent: Main, material: str) -> dict[str, dict[str, str]]:
    accuracy_profile = parent.color_settings_service.get_color_names_by_material(
        material
    )
    return {item["color"]: item for item in accuracy_profile if "color" in item}


@error_handler()
def get_defect_info_list(parent: Main, material: str) -> DefectsInfoList:
    if hasattr(parent, "camera"):
        parent.light.light_switch(True)
        image = parent.camera.long_exposure(50)
        parent.light.light_switch()
    else:
        latest_month = dt.today().strftime("%b%y")
        acc_file_list = dm.list_png_paths(dm.images_dir / latest_month)
        filtered_acc_file_list = [
            acc_file for acc_file in acc_file_list if material in acc_file.stem
        ]
        random_image_path = random.choice(filtered_acc_file_list)
        image = ImageManager.path_to_image(random_image_path)

    np_colors = [
        NPColorSpec(
            color_name=color_spec.color,
            is_tape=bool(color_spec.is_tape),
            lower_limit=np.array([int(x) for x in color_spec.lower_limit.split(",")]),
            upper_limit=np.array([int(x) for x in color_spec.upper_limit.split(",")]),
        )
        for color_spec in parent.color_specs
    ]
    calibration_mm_area = (
        math.pi * (int(parent.settings_data["cali_pin_size"]) / 2) ** 2
    )

    return process_defects(image, calibration_mm_area, np_colors)


@error_handler()
def on_num_pad(parent: Main, key: str, name: str) -> None:
    validate_lot_no_entry(parent)

    num_entry = NumPad(parent, mode=name).result
    defect_labels_widgets(parent, key).config(text=num_entry or 0)


@error_handler()
def on_blade_data(parent: Main, key: str, *args) -> None:
    validate_lot_no_entry(parent)

    if BladeData(parent, wos_lot_no_value(parent)).result:
        defect_labels_widgets(parent, key).config(bg="PaleGreen1", text="Added")


@error_handler()
def on_accuracy(parent: Main) -> None:
    validate_material_selection(parent)

    material = material_type_selection(parent)
    defects_info_list = get_defect_info_list(parent, material)

    image = defects_info_list.image
    color_data = defaultdict(lambda: {"count": 0, "area": 0})
    for defects_info in defects_info_list:
        cv2.drawContours(image, [defects_info.contour], -1, BGRColors.WHITE.value, 2)
        color = defects_info.color_name
        color_data[color]["count"] += 1
        color_data[color]["area"] += defects_info.mm_area

    acc_profile_lookup = accuracy_profile_lookup(parent, material)
    accuracy_results = [
        {
            "sticker_color": color,
            "sticker_count": acc_profile_lookup.get(color, {}).get("count", 0),
            "sticker_area": acc_profile_lookup.get(color, {}).get("area", 0),
            "count": data["count"],
            "area": data["area"],
        }
        for color, data in color_data.items()
    ]
    if not accuracy_results:
        CustomMessageBox(
            parent,
            "Accuracy Block Missing",
            "Accuracy block or stickers not found",
            "showerror",
        )
    Accuracy(parent, image, accuracy_results)


@error_handler()
def on_settings(parent: Main) -> None:
    cap = None
    image = None
    if hasattr(parent, "camera"):
        parent.light.light_switch(True)
        parent.camera.start_camera()
        cap = parent.camera.cap
    else:
        latest_month = dt.today().strftime("%b%y")
        acc_file_list = dm.list_png_paths(dm.images_dir / latest_month)
        random_image_path = random.choice(acc_file_list)
        image = ImageManager.path_to_image(random_image_path)
    if Settings(parent, cap=cap, image=image).result:
        parent.retrieve_db()
        if hasattr(parent, "camera"):
            parent.camera.stop_camera()
            parent.light.light_switch()


@error_handler()
def on_snap(parent: Main) -> None:
    validate_full_wos(parent)

    lot_no = wos_lot_no_value(parent)
    wos_entry = parent.widgets["wos_info"].cache
    block_data = {key: wos_entry[key].get() for key in wos_entry if key != "lot_no"}
    parent.lot_data_service.create_or_update_block_data(lot_no, block_data)

    chip_area = get_chip_area(parent)
    material = material_type_selection(parent)
    acc_profile_lookup = accuracy_profile_lookup(parent, material)
    defects_info_list = get_defect_info_list(parent, material)

    image = defects_info_list.image
    select_image = image.copy()

    tape_results = defaultdict(int)
    sticker_results = defaultdict(int)
    for defects_info in defects_info_list:
        color = defects_info.color_name
        contour = defects_info.contour
        defect_mode = acc_profile_lookup.get(color, {}).get("defect_mode")
        if not defect_mode:
            BlobHandler.draw_border_and_add_center_text(image, contour, "?")
            continue

        no_of_chips = math.ceil(defects_info.mm_area / chip_area)
        if defects_info.is_tape:
            color_key = f"{color}_{sum(color in name for name in tape_results)}"
            tape_results[color_key] = no_of_chips
            BlobHandler.draw_border_and_add_center_text(
                select_image, contour, len(tape_results)
            )
        else:
            sticker_results[defect_mode] += no_of_chips

    if tape_results:
        selected_results = Selector(parent, select_image, tape_results).result
        for color_key, defect_mode in selected_results.items():
            sticker_results[defect_mode] += tape_results[color_key]

    imagetk = TkinterImage.resize_numpy_to_tkinter(image, 0.75)
    image_holder_widgets(parent).imgtk = imagetk
    image_holder_widgets(parent).config(image=imagetk)

    defects_data = {}
    for defect_mode, no_of_chips in sticker_results.items():
        defect_key = reverse_defect_mapping[defect_mode]
        defects_data[defect_key] = no_of_chips
        defect_labels_widgets(parent, defect_key).config(text=str(no_of_chips))

    parent.lot_data_service.create_defects_data(lot_no, defects_data)


@error_handler()
def on_summary(parent: Main) -> None:
    validate_full_entry(parent)

    if Summary(
        parent,
        wos_lot_no_value(parent),
        wos_payroll_no_value(parent),
        wos_mc_no_value(parent),
        wos_input_qty_value(parent),
    ).result:
        CustomMessageBox(
            parent, "PRASS Completed", "Lot Successfully sent to PRASS.", "showinfo"
        )


buttons_map = {
    "accuracy": on_accuracy,
    "blade_data": on_blade_data,
    "num_pad": on_num_pad,
    "settings": on_settings,
    "snap": on_snap,
    "summary": on_summary,
}
