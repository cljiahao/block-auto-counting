import cv2
import numpy as np
from tkinter import PhotoImage
from pathlib import Path
from PIL import Image as PilImg, ImageTk


class TkinterImage:
    @staticmethod
    def _resize_and_convert(image: PilImg.Image, width: int, height: int) -> PhotoImage:
        """Resize image based on width and height argument and convert to PhotoImage"""
        resized_image = image.resize((width, height))
        return ImageTk.PhotoImage(resized_image)

    @staticmethod
    def _resize_from_aspect_ratio(
        image: PilImg.Image, win_size: dict[str, int | float], multiplier: float
    ) -> PhotoImage:
        image_aspect = image.width / image.height
        height = int(win_size["h_screen"] * multiplier)
        width = int(image_aspect * height)
        return width, height

    @staticmethod
    def resize_numpy_to_tkinter(
        image: np.ndarray, win_size: dict[str, int | float], multiplier: float
    ) -> PhotoImage:
        """Return resized and converted image to tkinter type"""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        tk_image = PilImg.fromarray(rgb_image)
        width, height = TkinterImage._resize_from_aspect_ratio(
            tk_image, win_size, multiplier
        )
        return TkinterImage._resize_and_convert(tk_image, width, height)

    @staticmethod
    def resize_path_to_tkinter(
        path: Path, win_size: dict[str, int | float], multiplier: float
    ) -> PhotoImage:
        """Resizes an image based on window size and multiplier, returning a PhotoImage object"""
        tk_image = PilImg.open(path)
        width, height = TkinterImage._resize_from_aspect_ratio(
            tk_image, win_size, multiplier
        )
        return TkinterImage._resize_and_convert(tk_image, width, height)
