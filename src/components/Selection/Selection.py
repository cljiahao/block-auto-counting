import math
from tkinter import Toplevel, Frame, Label, LabelFrame, Button, StringVar, OptionMenu
from tkinter import BOTH, SUNKEN, FLAT, NS, EW, NE, E, W

from utils.features import cvt_image


class Selection(Toplevel):
    """
    Selection Window Component to select non-established defects to stickers

    Parameters
    ----------
    settings : dict
        Settings
    screen_size : dict
        Providing Screen Size (Width and Height) to Class
    chip_area : float
        Area of chip in mm^2
    img : MatLike
        Image depicted with numbers to show which is point at
    to_select : widget
        Widget selection to be selected by user
    selected : dict
        Dict that holds the results of defects in pieces
    """

    def __init__(self, settings, screen_size, chip_area, img, to_select, selected):
        Toplevel.__init__(self)
        self.initialize(settings, img)
        self.win_config(screen_size)
        self.widgets(chip_area, to_select, selected)
        self.grab_set()
        self.mainloop()

    def initialize(self, settings, img):
        """Initialize variables"""
        self.set_names = settings["Names"]
        self.set_set = settings["Settings"]
        self.imgtk = cvt_image(img)

    def save_selected(self, chip_area, to_select, selected, drop_defect):
        """Check condition for selected and save them"""
        for key, value in to_select.items():
            for k in range(len(value)):
                chosen = drop_defect[key][k].get()
                pieces = math.ceil(sum(list(value[k].keys())) / chip_area)
                if chosen not in self.set_names["Defect Tape"]:
                    raise Exception("Empty Selection! Please Choose 1!")
                selected[chosen] = (
                    selected[chosen] + pieces if chosen in selected else pieces
                )
        self.destroy()
        self.quit()

    def win_config(self, screen_size):
        """Tkinter Window Config"""
        self.title("Select the defect mode")
        self.geometry(
            f"{int(screen_size['w_screen']*0.7)}x{int(screen_size['h_screen']*0.9)}+30+10"
        )
        self.frame = Frame(self)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(9, weight=1)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self, chip_area, to_select, selected):
        """Tkinter Widgets building"""
        # Display image on this container
        self.img_win = Label(self.frame, relief=SUNKEN, image=self.imgtk)
        self.img_win.grid(
            row=0, column=0, rowspan=19, columnspan=2, padx=5, pady=10, sticky=NS + EW
        )

        sel_defect = {}
        drop_defect = {}
        for i, key in enumerate(to_select.keys()):
            # FRAME: to hold OptionMenus for different stickers or tapes
            frame_select = LabelFrame(self.frame, bd=5, relief=FLAT, text=key)
            frame_select.grid(
                row=i, column=2, columnspan=2, ipadx=5, padx=5, pady=7, sticky=E
            )
            sel_defect[key] = {}
            drop_defect[key] = {}
            for j in range(len(to_select[key])):
                # Numbering of stickers / tapes
                Label(frame_select, text=f"[{j+1}]").grid(
                    row=j, column=0, pady=3, padx=10, sticky=W
                )
                # Drop down box to select defect modes
                sel_defect[key][j] = StringVar(value="Choose 1")
                drop_defect[key][j] = OptionMenu(
                    frame_select, sel_defect[key][j], *self.set_names["Defect Tape"]
                )
                drop_defect[key][j].config(width=13)
                drop_defect[key][j].grid(row=j, column=1, pady=3, sticky=W)

        # Button to save selected defect modes
        Button(
            self.frame,
            text="Save Changes",
            font=self.set_names["Font"]["M"],
            height=2,
            width=15,
            command=lambda: self.save_selected(
                chip_area, to_select, selected, sel_defect
            ),
        ).grid(
            row=10, column=len(["test"]) * 2, columnspan=2, pady=20, padx=10, sticky=NE
        )
