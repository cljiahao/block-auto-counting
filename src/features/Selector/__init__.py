import numpy as np
from tkinter import EW, NS
from tkinter import Toplevel

from components.ui.image_holder import ImageHolder
from features.Selector.widgets.buttons import SelectorButton
from features.Selector.widgets.dropdowns import DropDownContainer
from utils.tkinter.tk_utils import TkinterImage


class Selector(Toplevel):
    """
    A custom Tkinter Toplevel window to select defect modes for non stickers to tabulate into number of chips.

    Args:
        parent: The parent widget, usually Toplevel.
        to_select: List of strings to show in the dropdown box.
    """

    def __init__(self, parent: Toplevel, image: np.ndarray, to_select: list) -> None:
        super().__init__(parent)
        self.result: dict[str, str] = None
        self.widgets: dict[str, ImageHolder | DropDownContainer] = {}
        self.imgtk = TkinterImage.resize_numpy_to_tkinter(image, 0.75)
        self.win_config()
        self.add_widgets(to_select)
        # To ensure window stays on top and focused
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def win_config(self) -> None:
        self.title("Non-labelled Defect Selector")
        self.state("zoomed")
        self.rowconfigure(1, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self, to_select: list) -> None:
        self.widgets["image_holder"] = ImageHolder(self, self.imgtk)
        self.widgets["image_holder"].grid(
            row=0, column=0, rowspan=3, padx=5, pady=5, sticky=NS + EW
        )

        self.widgets["drop_down_cont"] = DropDownContainer(self, to_select)
        self.widgets["drop_down_cont"].grid(
            row=0, column=1, padx=5, pady=5, sticky=NS + EW
        )

        SelectorButton(self).grid(row=2, column=1, padx=5, pady=5, sticky=NS + EW)
