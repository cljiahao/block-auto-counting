import cv2
import math
import numpy as np

from pages.Main.utils.error import Custom_Exception


def cali_hough(settings, mat, img_arr):
    """
    Mask image to retrieve far left Black pin contour
    Parameters
    ----------
    settings : dict
        Settings
    img_arr : 3-D Image MAT Array
        Src input image array
    """
    pix_arr = []
    black_ll, black_ul = get_pin_col(settings, mat)
    for img in img_arr:
        get_pin(pix_arr, black_ll, black_ul, img)

    try:
        non_empty_arr = [x for x in pix_arr if x != ""]

        area_pixel = max(set(non_empty_arr), key=pix_arr.count)
        cali_area = (int(settings["Settings"]["Config"]["Pin Size"]) / 2) ** 2 * math.pi
        cali_pixel = cali_area / area_pixel
        print(f"Calibration Pin: {cali_pixel:.4f} mm^2/pixel")

        return img_arr[pix_arr.index(area_pixel)], cali_pixel
    except:
        raise Custom_Exception(
            {
                "title": "Calibration Error",
                "message": "Imaging Issue. \nPlease Try Again.",
            }
        )


def get_pin_col(settings, mat):
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


def get_pin(pix_arr, black_ll, black_ul, img):
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
                pix_arr.append(cnt_area)
    except:
        pix_arr.append("")
