from tkinter import EW, NS
from tkinter import Tk, Toplevel

from core.config import common_settings
from components.ui.image_holder import ImageHolder
from db.services.color_settings import ColorSettingsService
from db.services.configurations import ConfigurationsService
from db.services.lot_data import LotDataService
from db.session import get_db
from pages.Main.widgets.buttons import MainButtons
from pages.Main.widgets.defects_info import DefectDetails
from pages.Main.widgets.wos import WOSInfo
from utils.image_process.prep_cam import VideoCamera
from utils.lighting import LightingControl
from utils.tkinter.tk_windows import terminate


class Main(Toplevel):
    """
    A custom Tkinter Toplevel window to show the Main page / screen.

    Args:
        parent: The parent widget, usually Tk.
    """

    def __init__(self, parent: Tk):
        super().__init__(parent)
        self.widgets: dict[str, ImageHolder | DefectDetails | WOSInfo] = {}
        self.retrieve_db()
        self.win_config()
        self.add_widgets()
        # To ensure window stays on top and focused
        self.protocol("WM_DELETE_WINDOW", lambda: terminate(parent))
        self.grab_set()
        self.focus_set()

    def retrieve_db(self) -> None:
        db = next(get_db())

        self.lot_data_service = LotDataService(db)
        self.color_settings_service = ColorSettingsService(db)
        accuracy_profiles = self.color_settings_service.read_all_accuracy_profile()
        self.unique_materials = list(
            {profile.material for profile in accuracy_profiles}
        )
        self.color_specs = self.color_settings_service.read_all_color_specs()

        config_service = ConfigurationsService(db)
        self.chip_size_data = config_service.read_all_configurations_by_category(
            "chip_size"
        )
        self.settings_data = config_service.read_all_configurations_by_category(
            "settings"
        )
        if common_settings.TROUBLE == "false":
            if self.settings_data["troubleshoot"] == "false":
                self.camera = VideoCamera(
                    self.settings_data["camera_res_width"],
                    self.settings_data["camera_res_height"],
                )
                self.light = LightingControl(self)
            elif hasattr(self, "light"):
                self.light.close()
                self.camera.stop_camera()

    def win_config(self):
        self.title(common_settings.PROJECT_NAME)
        self.state("zoomed")
        self.rowconfigure(1, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self):
        self.widgets["image_holder"] = ImageHolder(self)
        self.widgets["image_holder"].grid(
            row=0, column=0, rowspan=4, padx=5, pady=3, sticky=NS + EW
        )

        self.widgets["defect_info"] = DefectDetails(self)
        self.widgets["defect_info"].grid(
            row=0, column=1, padx=5, pady=3, sticky=NS + EW
        )

        self.widgets["wos_info"] = WOSInfo(self)
        self.widgets["wos_info"].grid(row=2, column=1, padx=5, pady=3, sticky=NS + EW)

        MainButtons(self).grid(row=3, column=1, padx=5, pady=3, sticky=NS + EW)
