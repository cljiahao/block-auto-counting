from tkinter import Toplevel, Frame, Label, Button
from tkinter import BOTH, FLAT, NSEW, EW, W


class Final(Toplevel):
    """
    Final Window Component to display information for WOS

    Parameters
    ----------
    settings : dict
        Settings
    screen_size : dict
        Providing Screen Size (Width and Height) to Class
    lot_no : str
        Lot Number
    df : DataFrame

    """

    def __init__(self, settings, screen_size, lot_no, df):
        Toplevel.__init__(self)
        self.initialize(settings)
        self.win_config(screen_size)
        self.widgets(lot_no, df)
        self.grab_set()

    def initialize(self, settings):
        """Initialize variables"""
        self.set_names = settings["Names"]
        self.set_colors = settings["Colors"]
        self.set_set = settings["Settings"]

    def win_config(self, screen_size):
        """Tkinter Window Config"""
        self.title("To write on WOS")
        self.geometry(
            f"{int(screen_size['w_screen']*2/5)}x{int(screen_size['h_screen']*2/3)}+{int(screen_size['w_screen']*3/10)}+{int(screen_size['h_screen']*1/6)}"
        )
        self.frame = Frame(self)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self, lot_no, df):
        """Tkinter Widgets building"""
        l_font = self.set_names["Font"]["L"]
        xl_font = self.set_names["Font"]["XL"]

        # FRAME: for Lot Number
        frame_lot_no = Frame(self.frame, bd=5, relief=FLAT)
        frame_lot_no.grid(row=0, column=0, padx=3, pady=3, sticky=NSEW)

        # Lot Number
        Label(
            frame_lot_no,
            text=f"Lot Number: {lot_no}",
            font=xl_font,
        ).grid(row=0, column=0, padx=3, pady=3, sticky=W)

        # FRAME: for Final Data
        frame_data = Frame(self.frame, bd=5, relief=FLAT)
        frame_data.columnconfigure(2, weight=1)
        frame_data.grid(row=1, column=0, columnspan=2, padx=3, pady=3, sticky=NSEW)

        k, l = 0, 0
        for i, j in enumerate(df.index[:-1]):
            # Results Label
            Label(frame_data, text=j, font=l_font).grid(
                row=l, column=k, pady=3, padx=15, sticky=W
            )
            # Results Value
            Label(frame_data, text=df.loc[j][0], font=l_font).grid(
                row=l, column=k + 1, pady=3, padx=15, sticky=EW
            )

            if i % 2 == 0:
                k = 3
            else:
                k = 0
                l += 1

        # FRAME: for Button
        frame_button = Frame(self.frame, bd=5, relief=FLAT)
        frame_button.grid(row=0, column=1, padx=3, pady=3, sticky=EW)

        # Confirm Button to reset for next lot
        Button(
            frame_button,
            text="Okay",
            font=l_font,
            width=10,
            pady=5,
            bg="#93D976",
            command=lambda: self.destroy(),
        ).grid(row=0, column=0, sticky=EW)
