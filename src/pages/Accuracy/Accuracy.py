from tkinter import StringVar, Toplevel, Frame, Label, Entry, Canvas, Button
from tkinter import BOTH, SUNKEN, FLAT, RIDGE, CENTER, DISABLED, NS, EW, E, W

from utils.features import cvt_image


class Accuracy(Toplevel):
    """
    Accuracy Page for showing accuracy results processing accuracy blocks

    Parameters
    ----------
    settings : dict
        Settings
    screen_size : dict
        Providing Screen Size (Width and Height) to Class
    img : MatLike
        Image depicted with numbers to show which is point at
    calc_accuracy : dict
        Tabulated Num and Area values to each Colours
    mat : str
        Material Type
    """

    def __init__(self, settings, screen_size, img, calc_accuracy, mat):
        Toplevel.__init__(self)
        self.initialize(settings, img)
        self.win_config()
        self.widgets(screen_size, calc_accuracy, mat)

    def initialize(self, settings, img):
        """Initialize variables"""
        self.set_names = settings["Names"]
        self.set_colors = settings["Colors"]
        self.set_set = settings["Settings"]
        self.imgtk = cvt_image(img)
        self.acc_calc = {}
        self.acc_var = {}
        self.canva = {}

    def win_config(self):
        """Tkinter Window Config"""
        self.state("zoomed")
        self.title("Accuracy Check window")
        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self, screen_size, calc_accuracy, mat):
        """Tkinter Widgets building"""
        # Display image on this container
        self.img_win = Label(self.frame, relief=SUNKEN, image=self.imgtk)
        self.img_win.grid(
            row=0, column=0, rowspan=19, columnspan=2, padx=5, pady=10, sticky=NS + EW
        )

        # FRAME: for creating Label for Accuracy Name, Accuracy Actual and Calculated Quantity
        frame_acc = Frame(self.frame, bd=5, relief=FLAT)
        frame_acc.grid(row=0, column=3, columnspan=2, ipadx=5, padx=5, pady=7, sticky=E)

        # FRAME: for creating Buttons
        frame_button = Frame(self.frame, bd=5, relief=FLAT)
        frame_button.grid(
            row=18, column=3, columnspan=2, ipadx=5, padx=5, pady=7, sticky=E
        )

        accuracy = self.set_set["Accuracy"][mat]

        # Headers for each Color
        for i, state_label in enumerate(["Num", "Area"]):
            Label(frame_acc, font=self.set_names["Font"]["M"], text=state_label).grid(
                row=0, column=3 * (i + 1) - 3, columnspan=3, pady=5, sticky=EW
            )

        # Actual Accuracy, Processed results and pass/fail
        j = 1
        for col in accuracy.keys():
            # Skip color for optionmenu and if color value is empty
            if col == "Color" or len(accuracy[col]) < 1:
                continue
            self.acc_calc[col] = {}
            self.acc_var[col] = {}
            self.canva[col] = {}
            # Accuracy Name
            Label(frame_acc, font=self.set_names["Font"]["M"], text=col).grid(
                row=j, column=0, padx=10, pady=5, sticky=W
            )
            for k, state in enumerate(accuracy[col]):
                # Accuracy Calculated Quantity
                self.acc_var[col][state] = Label(
                    frame_acc, text=calc_accuracy[col][state], width=10, relief=RIDGE
                )
                self.acc_var[col][state].grid(
                    row=j, column=3 * (k + 1) - 2, pady=5, sticky=W
                )

                # Accuracy Actual Quantity
                self.acc_calc[col][state] = StringVar(value=accuracy[col][state])
                Entry(
                    frame_acc,
                    font=self.set_names["Font"]["M"],
                    textvariable=self.acc_calc[col][state],
                    width=12,
                    justify=CENTER,
                    state=DISABLED,
                ).grid(row=j, column=3 * (k + 1) - 1, padx=10, pady=5, sticky=W)

                # Red Green Light
                self.canva[col][state] = Canvas(
                    frame_acc,
                    width=int(1 / 40 * screen_size["w_screen"]),
                    height=int(1 / 24 * screen_size["h_screen"]),
                )
                self.canva[col][state].grid(row=j, column=3 * (k + 1), pady=5, sticky=W)
                self.canva[col][state].create_oval(
                    int(1 / 320 * screen_size["w_screen"]),
                    int(1 / 192 * screen_size["h_screen"]),
                    int(7 / 320 * screen_size["w_screen"]),
                    int(7 / 192 * screen_size["h_screen"]),
                )
                self.canva[col][state].addtag_withtag("circle", 1)

                # Return Green if pass, Red if fail
                pass_fail = (
                    "#93D976"
                    if abs(int(accuracy[col][state]) - int(calc_accuracy[col][state]))
                    < int(accuracy[col][state])
                    * float(self.set_set["Tolerance"]["Percentage"])
                    else "#fa6464"
                )
                self.canva[col][state].itemconfig("circle", fill=pass_fail)

            j += 1

        # Done Button to close
        Button(
            frame_button,
            text="Done",
            font=self.set_names["Font"]["M"],
            height=3,
            width=23,
            command=lambda: self.destroy(),
        ).grid(row=0, column=0, sticky=E)
