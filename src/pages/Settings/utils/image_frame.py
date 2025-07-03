from __future__ import annotations
from typing import TYPE_CHECKING

from utils.tkinter.tk_utils import TkinterImage

if TYPE_CHECKING:
    from pages.Settings import Settings

import cv2
import numpy as np


def filter_image_by_hsv(parent: Settings, image: np.ndarray):
    lower_limit = []
    upper_limit = []
    for key, value in parent.widgets["color_editor"].widgets["slider"].cache.items():
        str_val = value.get()
        (lower_limit.append(str_val) if "low" in key else upper_limit.append(str_val))

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    mask = cv2.inRange(
        hsv, np.array(lower_limit, np.uint8), np.array(upper_limit, np.uint8)
    )
    mask_3d = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    roi = cv2.bitwise_and(image, image, mask=mask)

    h1, w1 = roi.shape[:2]
    h2, w2 = mask_3d.shape[:2]

    # Combine masked and filtered image
    concat = np.zeros((h1 + h2, max(w1, w2), 3), dtype=np.uint8)
    concat[:, :] = (255, 255, 255)
    concat[:h1, :w1, :3] = roi
    concat[h1 : h1 + h2, :w2, :3] = mask_3d

    return TkinterImage.resize_numpy_to_tkinter(concat, parent.win_size, 0.75)
