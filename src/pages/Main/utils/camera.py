import os
import cv2
import random
from datetime import datetime as dt

from utils.calibration import cali_hough
from utils.directory import dire
from utils.features import get_defects


def camera(settings):
    res = settings["Settings"]["Config"]
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(res["CamResWidth"]))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(res["CamResHeight"]))
    return cap


def process_img(settings, light, mat, chip_type, troubleshoot, save_path):
    img_arr = prep_cam(settings, light, mat, troubleshoot)
    image, cali_pixel = cali_hough(settings, mat, img_arr)
    save_img(image, mat, save_path)
    defects, block = get_defects(settings, image, cali_pixel, chip_type, mat)
    return defects, block


def prep_cam(settings, light, mat, troubleshoot):
    img_arr = []
    if troubleshoot["Trouble"]:
        file_lists = os.listdir(dire.path_trouble)
        file_names = [fname for fname in file_lists if mat in fname]
        file_name = (
            random.sample(file_names, 1)[0]
            if troubleshoot["File Name"] == ""
            else troubleshoot["File Name"]
        )
        # TODO: Check if exists
        file_path = os.path.join(dire.path_trouble, file_name)
        img = cv2.imread(file_path)
        img_arr.append(img)

    else:
        light.light_switch(True)
        cap = camera(settings)
        for i in range(13):
            img = cap.read()[1]
            if i > 3:
                img_arr.append(
                    img[
                        :,
                        int(
                            int(settings["Settings"]["Config"]["CamResWidth"]) / 6
                        ) : int(
                            int(settings["Settings"]["Config"]["CamResWidth"]) / 6 * 5
                        ),
                    ]
                )
        cap.release()
        light.light_switch()

    return img_arr


def save_img(img, mat, save_path):
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
        if not os.path.exists(dire.path_trouble):
            os.makedirs(dire.path_trouble)
        file_path = os.path.join(
            dire.path_trouble, f"{mat}_{now.strftime('%d-%m-%y')}.png"
        )
        cv2.imwrite(file_path, img)
