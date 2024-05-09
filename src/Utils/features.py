import cv2
import numpy as np
import pandas as pd
from PIL import Image as PilImg, ImageTk


def cvt_image(img):
    """Return converted image color and Resize"""
    img = PilImg.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img = img.resize((int(img.size[0] * 0.75), int(img.size[1] * 0.75)))
    imgtk = ImageTk.PhotoImage(image=img)
    return imgtk


def get_defects(settings, image, cali_pixel, chip_type, mat):
    """Return defects processed and image"""
    # HSV range without Pin
    col_dict = get_col_dict(settings, mat)
    # Processed Block image from Camera
    block = find_block(image)
    # Stickers Mask from Block Image
    m_stickers = find_stickers(block, col_dict)
    # Dilate by factor for chip processing
    m_stickers = cv2.dilate(
        m_stickers,
        np.ones(
            (
                int(settings["Settings"]["Chip"][chip_type]["Factor"]),
                int(settings["Settings"]["Chip"][chip_type]["Factor"]),
            ),
            np.uint8,
        ),
    )
    contours, hier = cv2.findContours(
        m_stickers, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    # Defects processed and tabulated
    defects = get_defect_area(block, col_dict, cali_pixel, contours)

    return defects, block


def get_col_dict(settings, mat):
    """Return HSV Range without Pin"""
    col_dict = {}
    for colour, value in settings["Colors"].items():
        if colour == "Pin":
            continue
        if mat in value:
            Col_LL = np.array(
                [int(x) for x in value[mat]["LL"].split(",")],
                dtype=np.uint8,
            )
            Col_UL = np.array(
                [int(y) for y in value[mat]["UL"].split(",")],
                dtype=np.uint8,
            )
            col_dict[colour] = {"LL": Col_LL, "UL": Col_UL}

    return col_dict


# TODO: Find out how to get the numbers for cornerharris and ranges
def find_block(img):
    """Return block image without background from camera"""
    blank = np.zeros(img.shape[:2], np.uint8)
    kernel = np.ones((5, 5), np.uint8)

    blur = cv2.bilateralFilter(img.copy(), 9, 15, 15)

    for i in range(3):
        m_channel = cv2.adaptiveThreshold(
            blur[:, :, i],
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            15,
            3,
        )

        thresh = m_channel if i == 0 else cv2.add(thresh, m_channel)

    m_dilate = cv2.dilate(thresh, kernel)
    cnt, hier = cv2.findContours(m_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cn = sorted(cnt, key=lambda x: cv2.contourArea(x))[-1]
    m_drawn = cv2.drawContours(blank, [cn], -1, (255, 255, 255), -1)
    m_erode = cv2.erode(m_drawn, kernel)

    # Find Corners of Block to crop image properly
    crop_img = cv2.bitwise_and(img, img, mask=m_erode)
    dst = cv2.cornerHarris(m_erode, 25, 11, 0.03)
    ret, dst = cv2.threshold(dst, 0.2 * dst.max(), 255, 0)
    dst = np.uint8(dst)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

    # Sort the corners to crop image via OpenCV standards
    df = pd.DataFrame(stats, columns=list(range(len(stats[0]))))
    index = df[(df[4] < 500)].index
    cent = np.array([centroids[i].round(0).astype(int) for i in index])
    sum_cen = cent.sum(axis=1)
    x1, x2, y1, y2 = (
        cent[np.argmin(sum_cen)][0] - 3,
        cent[np.argmax(sum_cen)][0] + 3,
        cent[np.argmin(sum_cen)][1] - 3,
        cent[np.argmax(sum_cen)][1] + 3,
    )

    return crop_img[y1:y2, x1:x2]


def find_stickers(img, col_dict):
    """Return sticker mask image from block image"""
    hsv = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV_FULL)
    blur = cv2.bilateralFilter(hsv, 50, 15, 15)
    mix = np.zeros(img.shape[:2], np.uint8)

    # TODO: Able to adjust this parameter to find sticker / tape
    for col, col_range in col_dict.items():
        thresh = cv2.inRange(blur.copy(), col_range["LL"], col_range["UL"])
        if "Tape" in col:
            morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
            erode = cv2.erode(morph, np.ones((9, 9), np.uint8))
            mix = cv2.bitwise_or(mix, erode)
        else:
            erode = cv2.erode(thresh, None)
            morph = cv2.morphologyEx(erode, cv2.MORPH_OPEN, None)
            dilate = cv2.dilate(morph, None)
            mix = cv2.bitwise_or(mix, dilate)

    return mix


def get_defect_area(img, col_dict, cali_pixel, contours):
    """Return defect results and tabulation"""
    defects = {}
    blur = cv2.GaussianBlur(img.copy(), (5, 5), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV_FULL)
    for cnt in contours:
        cArea = cv2.contourArea(cnt)
        if 1000000 < cArea or cArea < 50:
            continue

        real_size = cArea * cali_pixel

        # Tabulate Sticker Colour and Size
        get_color_area(hsv, defects, col_dict, cnt, real_size)

    return defects


def get_color_area(hsv, defects, col_dict, cnt, real_size):
    """Return defect color and size"""
    blank = np.zeros(hsv.shape[:2], np.uint8)
    cv2.drawContours(blank, [cnt], 0, (255, 255, 255), -1)
    m_cnt = cv2.bitwise_and(hsv, hsv, mask=blank)
    for col, col_range in col_dict.items():
        m_sticker = cv2.inRange(m_cnt, col_range["LL"], col_range["UL"])
        if col not in defects:
            defects[col] = []
        if "Tape" in col and np.sum(m_sticker) < 30000:
            continue
        elif np.sum(m_sticker) > 10000:
            defects[col].append({real_size: cnt})
