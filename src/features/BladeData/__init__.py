from tkinter import EW, NS
from tkinter import Toplevel

from db.services.blade_data import BladeDataService
from db.session import get_db
from features.BladeData.widgets.buttons import BladeButton
from features.BladeData.widgets.input import BladeInput
from utils.tkinter.tk_windows import window_size


class BladeData(Toplevel):
    """
    A custom Tkinter Toplevel window to input BladeData information and return input after submit.

    Args:
        parent: The parent widget, usually Toplevel.
        lot_no: Lot number to tie the blade data input to.
    """

    def __init__(self, parent: Toplevel, lot_no: str) -> None:
        super().__init__(parent)
        self.result = None
        self.lot_no = lot_no
        self.widgets: dict[str, BladeInput] = {}
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
        self.blade_data_service = BladeDataService(db)

    def win_config(self) -> None:
        self.title("Blade Data Input Screen")
        self.win_size = window_size(self)
        x_position = int(self.win_size["w_screen"] / 3)
        y_position = int(self.win_size["h_screen"] / 5)
        self.geometry(f"+{x_position}+{y_position}")
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:

        self.widgets["blade_input"] = BladeInput(self)
        self.widgets["blade_input"].grid(
            row=0, column=0, padx=5, pady=5, sticky=NS + EW
        )

        BladeButton(self).grid(row=1, column=0, padx=5, pady=5, sticky=NS + EW)
