import numpy as np
from tkinter import EW, NS
from tkinter import Toplevel

from components.ui.image_holder import ImageHolder
from pages.Accuracy.widgets.sticker_summary import StickerSummary
from pages.Accuracy.widgets.buttons import AccuracyButton
from utils.tkinter.tk_utils import TkinterImage
from utils.tkinter.tk_windows import window_size


class Accuracy(Toplevel):
    """
    A custom Tkinter Toplevel window to show the results of processing accuracy block to actual data.

    Args:
        parent: The parent widget, usually Toplevel.
        acc_result: List
    """

    def __init__(self, parent: Toplevel, image: np.ndarray, acc_result: list) -> None:
        super().__init__(parent)
        self.result = None
        self.widgets: dict[str,] = {}
        self.imgtk = TkinterImage.resize_numpy_to_tkinter(image, 0.75)
        self.win_config()
        self.add_widgets(acc_result)
        # To ensure window stays on top and focused
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.grab_set()
        parent.wait_window(self)

    def win_config(self) -> None:
        self.title("Accuracy Check")
        self.state("zoomed")
        self.win_size = window_size(self)
        self.rowconfigure(1, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self, acc_result: list) -> None:
        self.widgets["image_holder"] = ImageHolder(self, self.imgtk)
        self.widgets["image_holder"].grid(
            row=0, column=0, rowspan=3, padx=5, pady=5, sticky=NS + EW
        )

        self.widgets["indicator"] = StickerSummary(self, acc_result)
        self.widgets["indicator"].grid(row=0, column=1, padx=5, pady=5, sticky=NS + EW)

        AccuracyButton(self).grid(row=2, column=1, padx=5, pady=5, sticky=NS + EW)
