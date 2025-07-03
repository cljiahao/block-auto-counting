import random
from cv2 import VideoCapture
from datetime import datetime as dt
from tkinter import EW, NS
from tkinter import Toplevel

import numpy as np

from components.ui.image_holder import ImageHolder
from core.directory_manager import directory_manager as dm
from db.services.color_settings import ColorSettingsService
from db.services.configurations import ConfigurationsService
from db.session import get_db
from pages.Settings.utils.image_frame import filter_image_by_hsv
from pages.Settings.widgets.buttons import SettingsButton
from pages.Settings.widgets.color_editor import ColorEditor
from pages.Settings.widgets.settings_info import SettingsInfo
from pages.Settings.widgets.config_tabs import ConfigTabs
from utils.image_process.image_manager import ImageManager
from utils.tkinter.tk_windows import window_size


class Settings(Toplevel):
    """
    A custom Tkinter Toplevel window to show the Settings page / screen.

    Args:
        parent: The parent widget, usually Toplevel.
    """

    def __init__(
        self, parent: Toplevel, cap: VideoCapture = None, image: np.ndarray = None
    ) -> None:
        super().__init__(parent)
        self.result = None
        self.cap = cap
        self.image = image
        self.widgets: dict[
            str, ImageHolder | ColorEditor | ConfigTabs | SettingsInfo
        ] = {}
        self.retrieve_db()
        self.win_config()
        self.add_widgets()
        self.show_frames()
        # To ensure window stays on top and focused
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.grab_set()
        parent.wait_window(self)

    def retrieve_db(self) -> None:
        db = next(get_db())
        self.color_settings_service = ColorSettingsService(db)
        self.config_service = ConfigurationsService(db)
        self.color_specs = self.color_settings_service.read_all_color_specs()
        self.color_names = [value.color for value in self.color_specs]

    def show_frames(self) -> None:
        if self.cap:
            _, image = self.cap.read()
        else:
            image = self.image
        imgtk = filter_image_by_hsv(self, image)

        self.widgets["image_holder"].widgets["image"].imgtk = imgtk
        self.widgets["image_holder"].widgets["image"].config(image=imgtk)
        self.widgets["image_holder"].widgets["image"].after(10, self.show_frames)

    def win_config(self) -> None:
        self.title("Settings")
        self.state("zoomed")
        self.win_size = window_size(self)
        self.rowconfigure(0, weight=2, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")
        self.rowconfigure(2, weight=1, uniform="a")
        self.columnconfigure(0, weight=4, uniform="a")
        self.columnconfigure(1, weight=8, uniform="a")
        self.columnconfigure(2, weight=3, uniform="a")

    def add_widgets(self) -> None:
        self.widgets["image_holder"] = ImageHolder(self)
        self.widgets["image_holder"].grid(
            row=0, column=0, rowspan=3, padx=5, pady=5, sticky=NS + EW
        )

        self.widgets["color_editor"] = ColorEditor(self)
        self.widgets["color_editor"].grid(
            row=0, column=1, padx=5, pady=5, sticky=NS + EW
        )

        self.widgets["config_tabs"] = ConfigTabs(self)
        self.widgets["config_tabs"].grid(
            row=1, column=1, rowspan=2, padx=5, pady=5, sticky=NS + EW
        )

        self.widgets["setting_info"] = SettingsInfo(self)
        self.widgets["setting_info"].grid(
            row=0, column=2, rowspan=2, padx=5, pady=5, sticky=NS + EW
        )

        SettingsButton(self).grid(row=2, column=2, padx=5, pady=5)
