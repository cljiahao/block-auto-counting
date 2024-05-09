import os
from datetime import datetime as dt
from tkinter import Tk, Frame, Label, Button, OptionMenu, StringVar
from tkinter import BOTH, CENTER, FLAT, EW, S

from pages.Main.components.defects import defect_list
from pages.Main.components.image import show_image
from pages.Main.components.wos import wos_entry
from pages.Main.utils.check import input_retrieve
from pages.Main.utils.routes import (
    show_accuracy,
    show_settings,
    show_summary,
    snap,
)
from utils.Lighting import Lighting
from utils.read_write import read_settings
from utils.directory import dire


class Main(Tk):
    """Main Page for Block Auto Counting"""

    def __init__(self):
        self.refresh()

    def refresh(self):
        """Refresh whole window when called"""
        Tk.__init__(self)
        self.initialize()
        self.win_config()
        self.widgets()

    def initialize(self):
        """Initialize variables"""
        self.settings = read_settings()
        self.set_names = self.settings["Names"]
        self.set_set = self.settings["Settings"]
        self.light = Lighting(self.settings)
        self.wos_var = {}
        self.excel_path = StringVar(value="")

    def cb_entry(self, input, name):
        """Call backs for Entry"""
        key = name.split(".")[-1]
        if key == "lot number" and len(input) == 10:
            input_retrieve(
                self.set_set["Address"]["QtyWeb"],
                input,
                self.wos_var["Input Quantity"],
                self.chip_type_var,
            )
            self.excel_path.set(
                os.path.join(
                    dire.path_excel, dt.today().strftime("%b%y"), input + ".xlsx"
                )
            )
            self.def_var["BLADE DATA"].config(text="Added", bg="#93D976")
            self.wos_var["Payroll Number"].focus()
        elif key == "payroll number" and len(input) == 7:
            self.wos_var["M/C Number"].focus()
        elif key == "m/c number" and len(input) == 3:
            self.wos_var["Input Quantity"].focus()
        return True

    def cb_color(self, name, index, mode):
        """Call backs for OptionMenu to set Color"""
        self.drop_acc.config(bg=self.set_set["Accuracy"][self.getvar(name)]["Color"])

    def win_config(self):
        """Tkinter Window Config"""
        self.title("Block Auto Cutting")
        self.state("zoomed")
        self.screen_size = {
            "h_screen": self.winfo_screenheight(),
            "w_screen": self.winfo_screenwidth(),
        }
        self.frame = Frame(self)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(len(self.set_names["Defect Code"]), weight=1)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self):
        """Tkinter Widgets building"""
        # Image container
        self.capture = show_image(self.frame, self.set_names)

        # FRAME: for creating Label for Defect Code, Defect Name, Defect Quantity
        frame_def = Frame(self.frame, bd=5, relief=FLAT)
        frame_def.grid(row=0, column=2, columnspan=2, pady=7, sticky=EW)

        # Defects Codes, Modes and Placeholders
        self.def_var = defect_list(
            frame_def, self.settings, self.wos_var, self.screen_size, self.excel_path
        )

        # FRAME: for holding WOS Scanning Entry boxes
        frame_wos = Frame(self.frame, bd=3, relief=FLAT)
        frame_wos.grid(
            row=len(self.set_names["Defect Code"]) + 1,
            column=2,
            columnspan=2,
            sticky=EW,
        )
        frame_wos.columnconfigure(3, weight=1)

        # Register for entry callbacks
        reg_entry = (self.register(self.cb_entry), "%P", "%W")

        # Entry Boxes for Lot no, Payroll no, Machine no and Lot Quantity
        wos_entry(frame_wos, self.set_names, self.wos_var, reg_entry)

        # FRAME: for holding Chip Type and Accuracy Spinner Box
        frame_type = Frame(self.frame, bd=3, relief=FLAT)
        frame_type.grid(
            row=len(self.set_names["Defect Code"]) + 3,
            column=2,
            columnspan=2,
            sticky=EW,
        )
        frame_type.columnconfigure(3, weight=1)

        # Chip Type
        self.chip_type_var = Label(
            frame_type, text="Chip Type", font=self.set_names["Font"]["L"], bg="#ecedcc"
        )
        self.chip_type_var.grid(row=0, column=1, columnspan=3, padx=(0, 10), pady=5)

        # Accuracy Dropdown Box
        sel_acc = StringVar(value=list(self.set_set["Accuracy"].keys())[0])
        self.drop_acc = OptionMenu(frame_type, sel_acc, *self.set_set["Accuracy"])
        self.drop_acc.config(
            width=int(self.screen_size["w_screen"] * 0.015),
            height=int(self.screen_size["h_screen"] * 0.0027),
            font=self.set_names["Font"]["M"],
            anchor=CENTER,
            bg="#c6e2e9",
        )
        self.drop_acc["menu"].config(font=self.set_names["Font"]["L"])
        self.drop_acc.grid(row=0, column=4, columnspan=3, padx=(0, 10), pady=5)

        # Register for optionmenu callbacks
        sel_acc.trace_add("write", self.cb_color)

        # FRAME: for holding Buttons
        frame_button = Frame(self.frame, bd=3, relief=FLAT)
        frame_button.grid(
            row=len(self.set_names["Defect Code"]) + 4,
            column=2,
            columnspan=6,
            sticky=EW,
        )

        # Summary Button
        Button(
            frame_button,
            text="Summary",
            height=2,
            width=15,
            command=lambda: show_summary(
                self.settings, self.screen_size, self.wos_var, self.excel_path.get()
            ),
        ).grid(row=0, column=0, padx=5, pady=3, sticky=S)

        # Accuracy Button
        Button(
            frame_button,
            text="Accuracy",
            height=2,
            width=15,
            command=lambda: show_accuracy(
                self.settings,
                self.screen_size,
                self.light,
                sel_acc.get(),
            ),
        ).grid(row=0, column=1, padx=5, pady=3, sticky=S)

        # Settings Button
        Button(
            frame_button,
            text="Settings",
            height=2,
            width=15,
            command=lambda: show_settings(
                self,
                self.settings,
                self.screen_size,
                self.light,
                sel_acc.get(),
                self.refresh,
            ),
        ).grid(row=0, column=2, padx=5, pady=3, sticky=S)

        # Snap Button
        Button(
            frame_button,
            text="Snap",
            height=2,
            width=35,
            font="sans 15 bold",
            bg="#ecedcc",
            command=lambda: snap(
                self.settings,
                self.screen_size,
                self.wos_var,
                self.def_var,
                self.excel_path.get(),
                self.light,
                self.chip_type_var,
                sel_acc.get(),
                self.capture,
            ),
        ).grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=EW + S)
