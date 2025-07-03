from tkinter import EW, NS
from tkinter import Toplevel

from db.services.color_settings import ColorSettingsService
from db.session import get_db
from features.NewColor.widgets.buttons import NewColorButtons
from features.NewColor.widgets.color_entry import ColorEntry
from features.NewColor.widgets.color_range import ColorRange
from utils.tkinter.tk_windows import window_size


class NewColor(Toplevel):
    """
    A custom Tkinter Toplevel window to input new color name and return input after submit.

    Args:
        parent: The parent widget, usually Toplevel.
        color_range: HSV color ranges adjusted by user to show.
    """

    def __init__(self, parent: Toplevel, color_range: dict[str, str]) -> None:
        super().__init__(parent)
        self.result = None
        self.color_range = color_range
        self.widgets: dict[str, ColorEntry | ColorRange] = {}
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

    def win_config(self) -> None:
        self.title("Add New Color")
        self.win_size = window_size(self)
        x_position = int(self.win_size["w_screen"] / 3)
        y_position = int(self.win_size["h_screen"] / 15)
        self.geometry(f"+{x_position}+{y_position}")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:

        self.widgets["color_entry"] = ColorEntry(self)
        self.widgets["color_entry"].grid(
            row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky=NS + EW
        )

        self.widgets["color_range"] = ColorRange(self)
        self.widgets["color_range"].grid(
            row=1, column=0, padx=5, pady=5, ipadx=5, ipady=5, sticky=NS + EW
        )

        NewColorButtons(self).grid(row=3, column=0, padx=5, pady=5, sticky=NS + EW)
