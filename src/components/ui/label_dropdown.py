from tkinter import DISABLED, EW, NORMAL, NS
from tkinter import Frame, Label, StringVar, Toplevel
from tkinter.ttk import Combobox
from typing import Callable


class LabelDropdown(Frame):
    """
    Tkinter Frame holding a label and dropdown box.

    Args:
        parent: Toplevel to place the frame into.
        label: Optional label string to show what the dropdown box is.
        value: Value placeholder to show on dropdown box.
        option: List of strings to show in the dropdown box.
        callback: Function to trigger callback when selection is made.
        disabled: Boolean flag to disabled combobox.
    """

    def __init__(
        self,
        parent: Toplevel,
        label: str = "",
        value: str = "Choose 1",
        option: list[str] = [""],
        callback: Callable = lambda *args, **kwargs: None,
        disabled: bool = False,
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.default = value or option[0]
        self.selection = StringVar(value=self.default)
        self.selection.trace_add(
            "write",
            lambda *args: callback(
                value=(
                    self.selection.get() if self.selection.get() != self.default else ""
                )
            ),
        )
        self.widgets: dict[str, Combobox] = {}
        self.win_config()
        self.add_widgets(label, option, disabled)

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=2, uniform="a")

    def add_widgets(self, label: str, option: list[str], disabled: bool) -> None:
        drop_col = 0
        drop_col_span = 2
        if label:
            Label(self, text=label).grid(row=0, column=0, sticky=NS + EW)
            drop_col = drop_col_span = 1

        self.widgets["combo_box"] = Combobox(
            self,
            textvariable=self.selection,
            values=option or [""],
            state=DISABLED if disabled else NORMAL,
        )
        self.widgets["combo_box"].grid(
            row=0, column=drop_col, columnspan=drop_col_span, sticky=NS + EW
        )
