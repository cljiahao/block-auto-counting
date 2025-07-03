from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from features.AccuracyProfile import AccuracyProfile

from tkinter import EW, NS
from tkinter import LabelFrame

from constants.block import defect_names
from components.ui.label_dropdown import LabelDropdown
from components.ui.label_entry import LabelEntry


class ProfileType(LabelFrame):
    """
    Tkinter LabelFrame holding ProfileType (material, defects mode) inputs and labels for AccuracyProfile component

    Args:
        parent: AccuracyProfile Toplevel.
    """

    def __init__(self, parent: AccuracyProfile) -> None:
        super().__init__(parent)
        self.parent = parent
        self.widgets: dict[str, LabelDropdown | LabelEntry] = {}
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

    def add_widgets(self) -> None:
        self.widgets["material"] = LabelDropdown(
            self,
            label="Material:",
            value=self.parent.material or "Select Material",
            option=(
                [
                    getattr(acc_profile, "material", "")
                    for acc_profile in self.parent.accuracy_profile
                ]
                if self.parent.accuracy_profile
                and self.parent.accuracy_profile[0] is not None
                else [""]
            ),
        )
        self.widgets["material"].grid(row=0, column=0, padx=10, pady=10, sticky=NS + EW)

        self.widgets["defect_mode"] = LabelDropdown(
            self,
            label="Defect Mode:",
            value=(
                self.parent.accuracy_profile[0].defect_mode
                if self.parent.material
                else "Select Defect Mode"
            ),
            option=[*defect_names, "None"],
        )
        self.widgets["defect_mode"].grid(
            row=1, column=0, padx=10, pady=10, sticky=NS + EW
        )
