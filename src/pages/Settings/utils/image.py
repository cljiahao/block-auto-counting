import cv2
import numpy as np
from PIL import Image, ImageTk


def filter_img(root, frame, entry_hsv):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)

    hsv_low = []
    hsv_high = []
    for key, value in entry_hsv.items():
        if "Low" in key:
            hsv_low.append(value.get() if value.get() else 0)
        else:
            hsv_high.append(value.get() if value.get() else 0)

    hsv_low = np.array(hsv_low, np.uint8)
    hsv_high = np.array(hsv_high, np.uint8)

    # Making mask for hsv range
    mask = cv2.inRange(hsv, hsv_low, hsv_high)
    vis = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Masking HSV value selected color becomes black
    rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = cv2.bitwise_and(rgbframe, rgbframe, mask=mask)

    h1, w1 = res.shape[:2]
    h2, w2 = vis.shape[:2]

    concat = np.zeros((h1 + h2, max(w1, w2), 3), dtype=np.uint8)
    concat[:, :] = (255, 255, 255)
    concat[:h1, :w1, :3] = res
    concat[h1 : h1 + h2, :w2, :3] = vis

    img = Image.fromarray(concat)
    width = int(root.winfo_height() / (img.size[1] / img.size[0]))
    height = root.winfo_height()
    if width == 0 or height == 0:
        width, height = (1, 1)
    img = img.resize((width, height))

    imgtk = ImageTk.PhotoImage(image=img)

    return imgtk
