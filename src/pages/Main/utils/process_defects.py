import math
import cv2
import numpy as np

from constants.colors import BGRColors
from core.logging import logger
from pages.Main.utils.utils_image_process import (
    filter_block_mask_by_mean_color,
    find_crop_block_image,
    refine_block_mask,
    find_calibration_pin,
    get_calibration_pin_area,
)
from schemas.contours import ContourInfo, ContourInfoList
from schemas.defects import NPColorSpec, DefectsInfo, DefectsInfoList
from utils.image_process.blob_handler import BlobHandler
from utils.image_process.contour_handler import ContourHandler


def process_defects(
    image: np.ndarray,
    calibration_mm_area: float,
    colors: list[NPColorSpec],
) -> DefectsInfoList:

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    calibration_mm_per_pixel = retrieve_calibration_pixel(
        gray_image, calibration_mm_area
    )

    crop_block_image = find_crop_block_image(image, gray_image)
    filtered_color_mask = filter_block_mask_by_mean_color(crop_block_image)
    refined_block_mask = refine_block_mask(filtered_color_mask)
    contour_info_list = find_sticker_contours(filtered_color_mask, refined_block_mask)

    defects_list = []
    hsv = cv2.cvtColor(crop_block_image, cv2.COLOR_BGR2HSV_FULL)
    for contour_info in contour_info_list:
        sticker_roi = extract_image_roi(hsv, contour_info)
        most_common_color = find_most_common_color(sticker_roi)

        found_color = ""
        is_tape = False
        for color in colors:
            if np.all(most_common_color >= color.lower_limit) and np.all(
                most_common_color <= color.upper_limit
            ):
                found_color = color.color_name
                is_tape = color.is_tape
                break

        defects_list.append(
            DefectsInfo(
                color_name=found_color,
                is_tape=is_tape,
                contour=contour_info.contour,
                mm_area=math.ceil(contour_info.area * calibration_mm_per_pixel),
            )
        )

    refined_block_image = cv2.bitwise_and(
        crop_block_image, crop_block_image, mask=refined_block_mask
    )

    return DefectsInfoList(image=refined_block_image, defects=defects_list)


def retrieve_calibration_pixel(
    gray_image: np.ndarray, calibration_mm_area: float
) -> float:
    width, height = gray_image.shape[:2]
    gray_roi = gray_image[int(height * 0.6) : int(height * 0.8), 0 : int(width / 4)]
    cali_pin = find_calibration_pin(gray_roi)

    calibration_pixel_area = get_calibration_pin_area(
        gray_roi, (cali_pin[0], cali_pin[1]), cali_pin[2]
    )
    calibration_mm_per_pixel = round(calibration_mm_area / calibration_pixel_area, 4)
    logger.info(f"Calibration Pin: {calibration_mm_per_pixel} mm^2/pixel")

    return calibration_mm_per_pixel


def find_sticker_contours(
    non_mean_bg_mask: np.ndarray, block_mask: np.ndarray
) -> ContourInfoList:
    inv_filtered_mask = cv2.bitwise_not(non_mean_bg_mask)
    patches_mask = cv2.bitwise_and(inv_filtered_mask, block_mask)

    open_kernel = BlobHandler.create_kernel(7)
    cleaned_mask = cv2.morphologyEx(patches_mask, cv2.MORPH_OPEN, open_kernel)

    contours, _ = cv2.findContours(
        cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    clean_contours = ContourHandler.filter_and_build_contour_info(contours)
    return ContourHandler.rotate_contour_upright(clean_contours)


def extract_image_roi(image: np.ndarray, contour: ContourInfo) -> np.ndarray:
    mask_roi = BlobHandler.draw_blob_mask_from_contour(image, contour.contour)
    image_roi = cv2.bitwise_and(image, image, mask=mask_roi)

    ((xc, yc), (width, height), _) = contour.rect
    return BlobHandler.crop_roi(image_roi, xc, yc, (width // 2 + 10, height // 2 + 10))


def find_most_common_color(image: np.ndarray) -> np.ndarray:
    reshape_image = image.reshape(-1, image.shape[-1])
    color_hexes, hex_count = np.unique(reshape_image, axis=0, return_counts=True)

    non_black_mask = ~np.all(color_hexes == BGRColors.BLACK.value, axis=1)

    non_black_counts = hex_count[non_black_mask]
    most_common_index = np.argmax(non_black_counts)

    non_black_colors = color_hexes[non_black_mask]
    return non_black_colors[most_common_index]
