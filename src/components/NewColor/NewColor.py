import re
import subprocess
from tkinter import (
    Toplevel,
    Frame,
    LabelFrame,
    Label,
    Button,
    messagebox,
)
from tkinter import BOTH, NS, EW

from components.common.checkbox import checkbox
from components.common.label_entry import label_entry
from components.common.optionmenu import dropdown


class NewColor(Toplevel):
    def __init__(self, root, ll_ul):
        Toplevel.__init__(self)
        self.initialize(root)
        self.win_config()
        self.widgets(ll_ul)
        self.grab_set()
        self.mainloop()

    def initialize(self, root):
        self.res = False
        self.set_names = root.set_names
        self.set_holder = root.set_holder
        self.set_set = root.set_set
        subprocess.Popen("osk", stdout=subprocess.PIPE, shell=True)

    def cb_entry(self, input, name):
        key = name.split(".")[-1]
        if key == "color":
            return bool(re.search(r"[^\W\d_]", input) or input == "")
        elif key == "num" or key == "area":
            return bool(re.search(r"\d", input) or input == "")

    def edit_col(self, text, ll_ul, mat, chips, mode, col_entry, acc_entry):
        if mat not in self.set_set["Accuracy"]:
            messagebox.showerror(
                title="Material not selected",
                message=f"Please Select an Option for Material",
                parent=self,
            )
            return

        # Add new Colours or Update
        col = col_entry.get()
        if (text == "new" and (col == "" or col in self.set_holder)) or (
            text == "update" and col not in self.set_holder
        ):
            col_entry.config(bg="#fa6464")
            return

        # Add new Accuracy
        acc_dict = {}
        for key, value in acc_entry.items():
            v = value.get()
            if text == "new" and (v == "" or col in self.set_set["Accuracy"][mat]):
                value.config(bg="#fa6464")
                return
            acc_dict[key] = v

        # Add new defect mode
        for chip in chips:
            def_modes = self.set_names["Defect Sticker"][chip]
            if (text == "new" and mode in def_modes.values()) or (
                text == "update"
                and mode in def_modes.values()
                and list(def_modes.keys())[list(def_modes.values()).index(mode)] != col
            ):
                messagebox.showerror(
                    title="Mode exists",
                    message=f"Modes exists with other colours, {list(def_modes.keys())[list(def_modes.values()).index(mode)]}: {mode}",
                    parent=self,
                )
                return

        # Update after all check is done
        if text == "new":
            self.set_set["Accuracy"][mat].update({col: acc_dict})
            self.set_holder[col] = {mat: ll_ul}
+
        for chip in self.set_names["Defect Sticker"]:
            if text == "remove" and col in self.set_names["Defect Sticker"][chip]:
                del self.set_names["Defect Sticker"][chip][col]
            if mode in self.set_names["Defect Code"]:
                if chip in chips:
                    self.set_names["Defect Sticker"][chip].update({col: mode})
                elif col in self.set_names["Defect Sticker"][chip]:
                    del self.set_names["Defect Sticker"][chip][col]

        self.res = True
        self.destroy()
        self.quit()

    def win_config(self):
        self.title("Add New Colour")
        self.geometry("+400+30")
        self.frame = Frame(self)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(9, weight=1)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self, ll_ul):
        reg_entry = (self.register(self.cb_entry), "%P", "%W")

        # LABELFRAME: Label frame for HSV
        frame_hsv = LabelFrame(self.frame)
        frame_hsv.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=NS + EW)

        # HSV Range
        Label(frame_hsv, text="HSV", font=self.set_names["Font"]["M"], width=10).grid(
            row=1, column=0, padx=10, pady=10, sticky=NS + EW
        )
        for i, key in enumerate(ll_ul.keys()):
            frame_hsv.columnconfigure(i + 1, weight=1)
            Label(frame_hsv, text=key, font=self.set_names["Font"]["M"]).grid(
                row=0, column=i + 1, padx=10, pady=10, sticky=NS + EW
            )
            Label(frame_hsv, text=ll_ul[key], font=self.set_names["Font"]["M"]).grid(
                row=1, column=i + 1, padx=10, pady=10, sticky=NS + EW
            )

        # LABELFRAME: Label Frame for Materia and Color
        frame_mat_col = LabelFrame(self.frame)
        frame_mat_col.columnconfigure(1, weight=1)
        frame_mat_col.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky=NS + EW
        )

        # Material tied to hsv range
        sel_mat = dropdown(
            frame_mat_col,
            "Material",
            "Select Material",
            self.set_set["Accuracy"],
            self.set_names["Font"]["M"],
            self.set_names["Font"]["M"],
            0,
            0,
        )

        col_entry = label_entry(
            frame_mat_col,
            "Color Name",
            ["Color"],
            self.set_names["Font"]["M"],
            2,
            0,
            reg_entry,
        )

        # LABELFRAME: Label Frame for Accuracy
        frame_acc = LabelFrame(self.frame)
        frame_acc.columnconfigure(1, weight=1)
        frame_acc.columnconfigure(2, weight=1)
        frame_acc.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=NS + EW)

        acc_entry = label_entry(
            frame_acc,
            "Accuracy",
            ["Num", "Area"],
            self.set_names["Font"]["M"],
            0,
            0,
            reg_entry,
        )

        # LABELFRAME: Label Frame for selecting chip type and defect mode
        frame_chip_mode = LabelFrame(self.frame)
        frame_chip_mode.columnconfigure(1, weight=1)
        frame_chip_mode.grid(
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky=NS + EW
        )

        # Defect Mode tied to chip type
        sel_chip = checkbox(
            frame_chip_mode,
            "Chip Type",
            self.set_names["Defect Sticker"],
            self.set_names["Font"]["M"],
            0,
            0,
        )

        # Chip type tied to defect mode
        sel_mode = dropdown(
            frame_chip_mode,
            "Defect Mode",
            "Select Defect Mode",
            self.set_names["Defect Code"],
            self.set_names["Font"]["M"],
            self.set_names["Font"]["M"],
            1,
            0,
        )

        # FRAME: Frame for buttons

        frame_buttons = Frame(self.frame)
        frame_buttons.columnconfigure(0, weight=1)
        frame_buttons.columnconfigure(1, weight=1)
        frame_buttons.grid(
            row=4, column=0, columnspan=2, padx=5, pady=5, sticky=NS + EW
        )

        # Update Button
        Button(
            frame_buttons,
            text="Update",
            font=self.set_names["Font"]["M"],
            command=lambda: self.edit_col(
                "update",
                ll_ul,
                sel_mat.get(),
                [i for i in sel_chip if sel_chip[i].get() == 1],
                sel_mode.get(),
                col_entry,
                acc_entry,
            ),
        ).grid(row=0, column=0, padx=10, pady=10, sticky=NS + EW)

        # Add New Button
        Button(
            frame_buttons,
            text="Add New",
            font=self.set_names["Font"]["M"],
            command=lambda: self.edit_col(
                "new",
                ll_ul,
                sel_mat.get(),
                [i for i in sel_chip if sel_chip[i].get() == 1],
                sel_mode.get(),
                col_entry,
                acc_entry,
            ),
        ).grid(row=0, column=1, padx=10, pady=10, sticky=NS + EW)
