import cv2
import numpy as np


# TODO: add docstrings
class VideoCamera:
    def __init__(self, res_width: int, res_height: int) -> None:
        self.cap = ""
        self.res_width = res_width
        self.res_height = res_height

    def start_camera(self) -> None:
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.res_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.res_height)

        if not self.cap.isOpened:
            raise IOError("Failed to open camera/video source.")

    def stop_camera(self) -> None:
        self.cap.release()
        self.cap = ""

    def long_exposure(self, exposure_limit: int) -> np.ndarray:
        self.start_camera()

        count = 0
        amass_image = None
        while count < exposure_limit:
            _, frame = self.cap.read()
            amass_image = amass_image + frame if amass_image else frame
            count += 1

        self.stop_camera()

        norm_bgr = amass_image / exposure_limit
        return np.clip(norm_bgr, 0, 255).astype(np.uint8)
