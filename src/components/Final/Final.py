from tkinter import Toplevel, Frame, Label, Button
from tkinter import BOTH, FLAT, NSEW, EW, W


class Final(Toplevel):
    def __init__(self, settings, screen_size, lot_no, df):
        Toplevel.__init__(self)
        self.initialize(settings)
        self.win_config(screen_size)
        self.widgets(lot_no, df)
        self.grab_set()

    def initialize(self, settings):
        self.set_names = settings["Names"]
        self.set_colors = settings["Colors"]
        self.set_set = settings["Settings"]

    def win_config(self, screen_size):
        self.title("To write on WOS")
        self.geometry(
            f"{int(screen_size['w_screen']*2/5)}x{int(screen_size['h_screen']*2/3)}+{int(screen_size['w_screen']*3/10)}+{int(screen_size['h_screen']*1/6)}"
        )
        self.frame = Frame(self)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self, lot_no, df):
        # FRAME: for Lot Number
        frame_lot_no = Frame(self.frame, bd=5, relief=FLAT)
        frame_lot_no.grid(row=0, column=0, padx=3, pady=3, sticky=NSEW)

        # Lot Number
        Label(
            frame_lot_no,
            text=f"Lot Number: {lot_no}",
            font=self.set_names["Font"]["XL"],
        ).grid(row=0, column=0, padx=3, pady=3, sticky=W)

        # FRAME: for Final Data
        frame_data = Frame(self.frame, bd=5, relief=FLAT)
        frame_data.columnconfigure(2, weight=1)
        frame_data.grid(row=1, column=0, columnspan=2, padx=3, pady=3, sticky=NSEW)

        # FRAME: for Button
        frame_button = Frame(self.frame, bd=5, relief=FLAT)
        frame_button.grid(row=0, column=1, padx=3, pady=3, sticky=EW)

        # Confirm Button to reset for next lot
        Button(
            frame_button,
            text="Okay",
            font=self.set_names["Font"]["L"],
            width=10,
            pady=5,
            bg="#93D976",
        ).grid(row=0, column=0, sticky=EW)
