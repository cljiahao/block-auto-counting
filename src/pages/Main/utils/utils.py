import os
import cv2
import pandas as pd
from tkinter import END
from datetime import datetime as dt


def reset(capture, def_var, wos_var, chip_type):
    """Reset Main Window"""
    capture.config(image="")
    # Reset defect mode and value
    def_reset(def_var)
    for i, wos in enumerate(wos_var.keys()):
        if i == 0:
            wos_var[wos].focus()
        wos_var[wos].delete(0, END)
    chip_type.config(text="Chip Type", bg="#ecedcc")


def def_reset(def_var):
    """Reset defect mode and value to update"""
    for def_mode in def_var:
        def_var[def_mode].config(text="0")


def save_excel(excel_path, def_var, numpad=False):
    """Save data into excel for easy retrieval"""
    # TODO: Convert to database instead?

    if not os.path.exists(os.path.dirname(excel_path)):
        os.makedirs(os.path.dirname(excel_path))

    def_dict = {k: v.cget("text") for k, v in def_var.items()}
    df = (
        pd.read_excel(excel_path, index_col=0, header=None)
        if os.path.exists(excel_path)
        else pd.DataFrame.from_dict(def_dict, orient="index")
    )
    if numpad:
        df = df.iloc[:, :-1]

    new_df = pd.DataFrame.from_dict(def_dict, orient="index")
    result = df if df.equals(new_df) else pd.concat([df, new_df], axis=1)
    result = result.fillna(0)
    result.to_excel(excel_path, header=False)


def saveImg(self, img, timestp):
    """Save Image to month year folder"""
    if not self.ini_config["Trouble"]:
        imgdir = os.path.join(self.path_block, dt.today().strftime("%b%y"))
        if not os.path.exists(imgdir):
            os.makedirs(imgdir)
        imgfile = os.path.join(imgdir, timestp + ".png")
        if not os.path.exists(imgfile):
            cv2.imwrite(imgfile, img)


def draw_img(img, contours, values=False):
    """Draw on image based on requirements"""
    w_img, h_img = img.shape[:2]
    buffer = 50
    for i, cnt in enumerate(contours):
        ((cx, cy), (width, height), angle) = cv2.minAreaRect(cnt)

        value = str(round(values[i], 1)) if values else str(i + 1)
        cx = check_limits(cx, w_img, buffer)
        cy = check_limits(cy, h_img, buffer)

        cv2.putText(
            img,
            value,
            (int(cx), int(cy)),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0, 255, 255),
            1,
        )

        cv2.drawContours(img, [cnt], -1, (255, 255, 255), 1)

    return img


def check_limits(center, limit, buffer):
    """Prevent drawn text out of bounds"""
    if center - buffer < 0:
        center = center + buffer
    elif limit < center + buffer:
        center = center - buffer
    else:
        center = center + 10
    return center
