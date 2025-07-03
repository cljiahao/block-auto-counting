from tkinter import EW, NS
from tkinter import Toplevel

from db.services.color_settings import ColorSettingsService
from db.session import get_db
from features.AccuracyProfile.widgets.accuracy import AccuracyEntry
from features.AccuracyProfile.widgets.buttons import EditAccuracyButtons
from features.AccuracyProfile.widgets.color_label import ColorLabel
from features.AccuracyProfile.widgets.profile_type import ProfileType
from utils.tkinter.tk_windows import window_size


class AccuracyProfile(Toplevel):
    """
    A custom Tkinter Toplevel window to input or update accuracy profile into database.

    Args:
        parent: The parent widget, usually Toplevel.
        color_name: Name of color to tie the accuracy profile to in database.
        material: Optional name of material to update accuracy profile with.
    """

    def __init__(self, parent: Toplevel, color_name: str, material: str = "") -> None:
        super().__init__(parent)
        self.result = None
        self.color_name = color_name
        self.material = material
        self.widgets: dict[str, AccuracyEntry | ProfileType] = {}
        self.retrieve_db()
        self.win_config()
        self.add_widgets()
        # To ensure window stays on top and focused
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def retrieve_db(self) -> None:
        db = next(get_db())
        self.color_settings_service = ColorSettingsService(db)
        self.accuracy_profile = (
            self.color_settings_service.read_accuracy_profile_not_empty(
                self.color_name, self.material
            )
        )

    def win_config(self) -> None:
        self.title(f"{'Add New' if self.material else 'Update'} Accuracy Profile")
        self.win_size = window_size(self)
        x_position = int(self.win_size["w_screen"] / 3)
        y_position = int(self.win_size["h_screen"] / 15)
        self.geometry(f"+{x_position}+{y_position}")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:

        ColorLabel(self).grid(row=0, column=0, padx=5, pady=5, sticky=NS + EW)

        self.widgets["accuracy_entry"] = AccuracyEntry(self)
        self.widgets["accuracy_entry"].grid(
            row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky=NS + EW
        )

        self.widgets["profile_type"] = ProfileType(self)
        self.widgets["profile_type"].grid(
            row=2, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky=NS + EW
        )

        EditAccuracyButtons(self).grid(row=3, column=0, padx=5, pady=5, sticky=NS + EW)
