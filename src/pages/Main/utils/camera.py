import os
import cv2
import random
from datetime import datetime as dt

from utils.calibration import cali_hough
from core.directory import dire
from utils.features import get_defects


def camera(settings):
    """Return cam after setting resolution"""
    res = settings["Settings"]["Config"]
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(res["CamResWidth"]))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(res["CamResHeight"]))
    return cap


def process_img(settings, light, mat, chip_type, troubleshoot, save_path):
    """Main function to process image. Return defects results and block image with drawings."""
    img = prep_cam(settings, light, mat, troubleshoot)
    cali_pixel = cali_hough(settings, mat, img)
    save_img(img, mat, save_path)
    defects, block = get_defects(settings, img, cali_pixel, chip_type, mat)
    return defects, block


def prep_cam(settings, light, mat, troubleshoot):
    """Return arr of images for calibration to choose best image"""
    if troubleshoot["Trouble"]:
        file_lists = os.listdir(dire.trouble_dir)
        file_names = [fname for fname in file_lists if mat in fname]
        file_name = (
            random.sample(file_names, 1)[0]
            if troubleshoot["File Name"] == ""
            else troubleshoot["File Name"]
        )
        # TODO: Check if exists
        file_path = os.path.join(dire.trouble_dir, file_name)
        img = cv2.imread(file_path)

    else:
        light.light_switch(True)
        cap = camera(settings)
        base_img_bgr = {"B": 0, "G": 0, "R": 0, "count": 0}
        for _ in range(50):
            img = cap.read()[1]
            new_img = img[
                :,
                int(int(settings["Settings"]["Config"]["CamResWidth"]) / 6) : int(
                    int(settings["Settings"]["Config"]["CamResWidth"]) / 6 * 5
                ),
            ]
            long_exposure(base_img_bgr, new_img)

        total = base_img_bgr.pop("count")
        bgr_arr = [color / total for color in base_img_bgr.values()]
        img = cv2.merge(bgr_arr).astype("uint8")

        cap.release()
        light.light_switch()

    return img


def long_exposure(base_img_bgr, new_img):
    """Create long exposure to sharpen image"""

    (B, G, R) = cv2.split(new_img.astype("float"))

    base_img_bgr["B"] += B
    base_img_bgr["G"] += G
    base_img_bgr["R"] += R
    base_img_bgr["count"] += 1


def save_img(img, mat, save_path):
    """Save image function"""
    # Save to respective save_path
    now = dt.today()
    folder_path = os.path.join(save_path, now.strftime("%b%y"))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, f"{mat}_{now.strftime('%d-%m-%y')}.png")
    cv2.imwrite(file_path, img)

    # Save to trouble with a random small chance for troubleshooting
    rand_digit = random.randrange(0, 1000) / 1000
    if rand_digit < 0.05:
        if not os.path.exists(dire.trouble_dir):
            os.makedirs(dire.trouble_dir)
        file_path = os.path.join(
            dire.trouble_dir, f"{mat}_{now.strftime('%d-%m-%y')}.png"
        )
        cv2.imwrite(file_path, img)
