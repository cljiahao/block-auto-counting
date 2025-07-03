from collections import defaultdict
from tkinter import EW, NS, S, W
from tkinter import Label, StringVar, Toplevel
from tkinter.ttk import Separator

from constants.common import font_size
from db.services.blade_data import BladeDataService
from db.services.lot_data import LotDataService
from db.session import get_db
from pages.Summary.widgets.defect_summary import DefectSummary
from pages.Summary.widgets.buttons import SummaryButtons


class Summary(Toplevel):
    """
    A custom Tkinter Toplevel window to show overall cached data based on lot number on the Summary page / screen.

    Args:
        parent: The parent widget, usually Toplevel.
    """

    def __init__(
        self, parent: Toplevel, lot_no: str, payroll_no: str, mc_no: str, input_qty: str
    ) -> None:
        super().__init__(parent)
        self.result = None
        self.lot_no = lot_no
        self.payroll_no = payroll_no
        self.mc_no = mc_no
        self.input_qty = input_qty
        self.widgets: dict[str, DefectSummary] = {}
        self.cache: dict[str, StringVar] = {}
        self.retrieve_db()
        self.win_config()
        self.add_widgets()
        # To ensure window stays on top and focused
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.grab_set()
        parent.wait_window(self)

    def retrieve_db(self) -> None:
        db = next(get_db())
        self.blade_data_service = BladeDataService(db)
        self.lot_data_service = LotDataService(db)
        self.lot_data = self.lot_data_service.read_block_data_not_empty(self.lot_no)
        self.defects_dict = defaultdict(list)
        for defects_data in self.lot_data.defects_data:
            for key, value in defects_data.__dict__.items():
                self.defects_dict[key].append(value)

    def win_config(self) -> None:
        self.title("Summary")
        self.state("zoomed")
        self.rowconfigure(1, weight=1, uniform="a")
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")

    def add_widgets(self) -> None:
        Label(self, text=f"Lot Number : {self.lot_no}", font=font_size["m"]).grid(
            row=0, column=0, padx=3, pady=5, sticky=W
        )

        SummaryButtons(self).grid(row=0, column=1, padx=3, pady=5, sticky=NS + EW)

        Separator(self, orient="horizontal").grid(
            row=0,
            column=0,
            columnspan=2,
            pady=3,
            sticky=EW + S,
        )

        self.widgets["defect_summary"] = DefectSummary(self)
        self.widgets["defect_summary"].grid(
            row=1, column=0, columnspan=2, padx=3, pady=3, sticky=NS + EW
        )
