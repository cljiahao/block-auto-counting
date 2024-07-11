import os
import pandas as pd
from tkinter import Toplevel, Frame, Label, Button, messagebox
from tkinter import BOTH, FLAT, EW, S, E, W
from tkinter.ttk import Separator

from components.Final.Final import Final
from pages.Summary.utils.prass import send_PRASS
from utils.read_write import read_json


class Summary(Toplevel):
    """Summary Page to show Overall Summary of Lot and to send to PRASS

    Parameters
    ----------
    settings : dict
        Settings
    screen_size : dict
        Providing Screen Size (Width and Height) to Class
    wos_var : dict
        Dictionary of Entry (Lot No, Payroll No, Machine No and Lot Quantity)
    excel_path : str
        Excel File Path
    """

    def __init__(self, settings, screen_size, wos_var, excel_path):
        self.initialize(settings, screen_size, wos_var, excel_path)
        self.reset()

    def reset(self):
        """Refresh whole window when called"""
        Toplevel.__init__(self)
        self.win_config()
        self.widgets()
        self.grab_set()

    def initialize(self, settings, screen_size, wos_var, excel_path):
        """Initialize variables"""
        self.res = True
        self.settings = settings
        self.set_names = settings["Names"]
        self.set_colors = settings["Colors"]
        self.set_set = settings["Settings"]
        self.blade_data = read_json("core/json/blade_data.json")
        self.screen_size = screen_size
        self.wos_var = wos_var
        self.lot_no = wos_var["Lot Number"].get()
        self.excel_path = excel_path

    def confirm(self, df):
        """Checks condition and send data to PRASS"""
        # Check if Blade Data added to Lot No
        if self.lot_no not in self.blade_data:
            messagebox.showerror(
                title="No Blade Data", message="Please input blade data"
            )
            return

        # Retrieve blade data
        blade = self.blade_data[self.lot_no]

        if messagebox.askyesno(
            title="Send Data To PRASS", message="Confirm Send Data?"
        ):
            # Send to Prass
            new_df, res = send_PRASS(self.settings, self.wos_var, df, blade)
            if res:
                # Show Final Page Window to write on WOS
                Final(
                    self.settings,
                    self.screen_size,
                    self.lot_no,
                    new_df,
                )
                self.destroy()

    def delete(self, df, index):
        """Delete column of data"""
        df.drop(df.columns[[index]], axis=1, inplace=True)
        df.to_excel(self.excel_path, index=False, header=False)
        self.destroy()
        self.reset()

    def win_config(self):
        """Tkinter Window Config"""
        self.title("Summary Window")
        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self):
        """Tkinter Widgets building"""
        # FRAME: for creating Label for Lot Number Information
        frame_lot_no = Frame(self.frame, bd=5, relief=FLAT)
        frame_lot_no.grid(row=0, column=0, padx=3, pady=1, sticky=W)

        # Lot Number Text
        Label(
            frame_lot_no,
            text=f"Lot Number : {self.lot_no}",
            font=self.set_names["Font"]["S"],
        ).grid(row=0, column=0, pady=1, sticky=W)

        # FRAME: for creating Label for Defects Data Processed
        frame_data = Frame(self.frame, bd=5, relief=FLAT)
        frame_data.grid(row=1, column=0, pady=1, padx=10)

        # Block Number
        block_no = Label(frame_data, font=self.set_names["Font"]["S"], text="Block No")
        block_no.grid(row=0, column=0, pady=1, padx=15, sticky=W)

        if os.path.exists(self.excel_path):
            # Read Excel into Dataframe
            df = pd.read_excel(self.excel_path, header=None)

            max_rows, max_cols = df.shape

            # Add Seperator between Header and Main
            Separator(self.frame, orient="horizontal").grid(
                row=0, column=0, columnspan=max_cols, sticky=EW + S
            )
            # Dynamically Expand window depending on number of columns
            x_val = 300 if max_cols * 90 < 300 else max_cols * 90
            if self.screen_size["w_screen"] < x_val * 1.1:
                self.state("zoomed")
            else:
                self.geometry(
                    str(x_val) + f"x{int(self.screen_size['h_screen']*0.85)}+0+0"
                )

            for i in range(max_cols):
                for j in range(max_rows):
                    # Values in dataframe
                    Label(
                        frame_data,
                        text=df.iloc[j, i],
                        font=self.set_names["Font"]["S"],
                    ).grid(row=j + 1, column=i, padx=15, sticky=W)
                if i == 0:
                    # Confirm Button to send to PRASS
                    Button(
                        frame_data,
                        text="Confirm",
                        font=self.set_names["Font"]["S"],
                        width=10,
                        bg="#3085d6",
                        command=lambda: self.confirm(df),
                    ).grid(row=max_rows + 1, column=i, pady=5, padx=15, sticky=S)
                    continue
                # Block Number
                Label(frame_data, text=f"Block {i}").grid(
                    row=0, column=i, pady=1, padx=15, sticky=E
                )
                # Delete Button to remove specific block
                Button(
                    frame_data,
                    text="x",
                    font=self.set_names["Font"]["S"],
                    width=2,
                    height=1,
                    bg="#fa6565",
                    command=lambda index=i: self.delete(df, index),
                ).grid(row=max_rows + 1, column=i, pady=5, padx=15, sticky=W)
