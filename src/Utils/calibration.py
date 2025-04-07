import cv2
import math
import numpy as np

from pages.Main.utils.error import Custom_Exception
from core.logging import logger


def cali_hough(settings, mat, img):
    """Mask image to retrieve far left Black pin contour"""
    # Get HSV Range for Pin
    black_ll, black_ul = get_pin_col(settings, mat)
    # Tabulate Pin Pixel
    area_pixel = get_pin(black_ll, black_ul, img)

    try:
        # Get Best Pin Pixel and image
        cali_area = (int(settings["Settings"]["Config"]["Pin Size"]) / 2) ** 2 * math.pi
        cali_pixel = f"{cali_area / area_pixel:.4f}"
        logger.info("Calibration Pin: %s mm^2/pixel", cali_pixel)

        return cali_pixel
    except:
        raise Custom_Exception(
            {
                "title": "Calibration Error",
                "message": "Imaging Issue. \nPlease Try Again.",
            }
        )


def get_pin_col(settings, mat):
    """Return HSV Range for Pin"""
    pin_col = settings["Colors"]["Pin"][mat]
    black_ll = np.array(
        [int(x) for x in pin_col["LL"].split(",")],
        dtype=np.uint8,
    )
    black_ul = np.array(
        [int(y) for y in pin_col["UL"].split(",")],
        dtype=np.uint8,
    )

    return black_ll, black_ul


def get_pin(black_ll, black_ul, img):
    """Return Pin ROI in image"""
    # TODO: Fixed Area for calibration pin
    img = img[800:950, 50:250]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blank = np.zeros(img.shape[:2], np.uint8)

    # TODO: Hough Circle Parameters
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        2,
        20,
        param1=20,
        param2=60,
        minRadius=3,
        maxRadius=13,
    )
    try:
        for c in circles[0]:
            cv2.circle(blank, (int(c[0]), int(c[1])), int(c[2]), (255, 255, 255), -1)

        circle_mask = cv2.bitwise_and(img, img, mask=blank)

        cnts, _ = cv2.findContours(blank, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        blur = cv2.GaussianBlur(circle_mask, (5, 5), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV_FULL)
        black = cv2.inRange(hsv, black_ll, black_ul)

        for c in cnts:
            cnt_area = cv2.contourArea(c)
            if cnt_area > 300 and np.sum(black) > 10000:
                return cnt_area
    except:
        return ""
