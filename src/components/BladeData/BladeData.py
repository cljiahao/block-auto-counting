import subprocess
from tkinter import Toplevel, Frame, Label, Entry, Button, StringVar, OptionMenu
from tkinter import BOTH, CENTER, FLAT, NS, EW

from utils.read_write import read_json, write_json


class BladeData(Toplevel):
    """
    Blade Data Component to input blade data information

    Parameters
    ----------
    settings : dict
        Settings
    lot_no : str
        Lot Number
    label : widget
        Label Widget to update the label text
    """

    def __init__(self, settings, lot_no, label):
        Toplevel.__init__(self)
        self.initialize(settings, lot_no, label)
        self.win_config()
        self.widgets()
        self.grab_set()

    def initialize(self, settings, lot_no, label):
        """Initialize variables"""
        self.set_names = settings["Names"]
        self.lot_no = lot_no
        self.label = label
        self.blade_data = read_json("json/blade_data.json")
        # Open Window's Keyboard
        subprocess.Popen("osk", stdout=subprocess.PIPE, shell=True)

    def confirm(self):
        """To Confirm data and write it to json for holding"""
        if self.lot_no not in self.blade_data:
            self.blade_data[self.lot_no] = {}
        self.sel_blade.update(self.entry_blade)
        for txt, value in self.sel_blade.items():
            self.blade_data[self.lot_no][txt] = value.get().strip()
        write_json("json/blade_data.json", self.blade_data)
        self.label.config(text="Added", bg="#93D976")
        self.destroy()

    def win_config(self):
        """Tkinter Window Config"""
        self.title("Blade Data Input Screen")
        self.geometry("+50+50")
        self.frame = Frame(self)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self):
        """Tkinter Widgets building"""
        # FRAME: for Blade Data
        frame_blade = Frame(self.frame, bd=5, relief=FLAT)
        frame_blade.columnconfigure(1, weight=1)
        frame_blade.grid(row=0, column=0, padx=5, pady=5, sticky=NS + EW)

        self.entry_blade = {}
        self.sel_blade = {}

        for i, txt in enumerate(self.set_names["Blade Data"]):
            frame_blade.rowconfigure(i, weight=1)
            # Retrieve previous data is exist in json file
            value = (
                self.blade_data[self.lot_no][txt]
                if self.lot_no in self.blade_data
                else self.set_names["Blade Data"][txt][0]
            )
            # Blade Data Label
            Label(
                frame_blade,
                text=txt,
                font=self.set_names["Font"]["L"],
            ).grid(row=i, column=0, padx=10, pady=10, sticky=NS + EW)

            if isinstance(self.set_names["Blade Data"][txt], list):
                # Drop Down box for name and type selection
                self.sel_blade[txt] = StringVar(value=value)
                drop_blade = OptionMenu(
                    frame_blade, self.sel_blade[txt], *self.set_names["Blade Data"][txt]
                )
                drop_blade.config(
                    font=self.set_names["Font"]["L"],
                )
                drop_blade["menu"].config(font=self.set_names["Font"]["L"])
                drop_blade.grid(row=i, column=1, padx=10, pady=10, sticky=EW)
            else:
                # Entry box to input batch no and life span
                self.entry_blade[txt] = Entry(
                    frame_blade,
                    name=txt.lower(),
                    font=self.set_names["Font"]["L"],
                    justify=CENTER,
                )
                self.entry_blade[txt].insert(0, value)
                self.entry_blade[txt].grid(row=i, column=1, padx=10, pady=10, sticky=EW)

        # Button to save input to holder
        Button(
            frame_blade,
            text="Submit",
            font=self.set_names["Font"]["L"],
            command=lambda: self.confirm(),
        ).grid(row=i + 1, column=1, padx=5, pady=5, ipadx=3, ipady=3, sticky=NS + EW)
