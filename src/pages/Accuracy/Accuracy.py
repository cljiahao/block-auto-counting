from tkinter import StringVar, Toplevel, Frame, Label, Entry, Canvas, Button
from tkinter import BOTH, SUNKEN, FLAT, RIDGE, CENTER, DISABLED, NS, EW, E, W

from utils.features import cvt_image


class Accuracy(Toplevel):
    def __init__(self, settings, screen_size, img, calc_accuracy, mat):
        Toplevel.__init__(self)
        self.initialize(settings, img)
        self.win_config()
        self.widgets(screen_size, calc_accuracy, mat)

    def initialize(self, settings, img):
        self.set_names = settings["Names"]
        self.set_colors = settings["Colors"]
        self.set_set = settings["Settings"]
        self.imgtk = cvt_image(img)
        self.acc_calc = {}
        self.acc_var = {}
        self.canva = {}

    def win_config(self):
        self.state("zoomed")
        self.title("Accuracy Check window")
        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self, screen_size, calc_accuracy, mat):
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
        i = 0
        for col in accuracy.keys():
            if col == "Color":
                continue
            self.acc_calc[col] = {}
            self.acc_var[col] = {}
            self.canva[col] = {}
            for state in accuracy[col]:
                # Accuracy Name
                Label(
                    frame_acc, font=self.set_names["Font"]["M"], text=f"{col}_{state}"
                ).grid(row=i, column=0, padx=10, pady=5, sticky=W)

                # Accuracy Calculated Quantity
                self.acc_var[col][state] = Label(
                    frame_acc, text=calc_accuracy[col][state], width=10, relief=RIDGE
                )
                self.acc_var[col][state].grid(row=i, column=1, pady=5, sticky=W)

                # Accuracy Actual Quantity
                self.acc_calc[col][state] = StringVar(value=accuracy[col][state])
                Entry(
                    frame_acc,
                    font=self.set_names["Font"]["M"],
                    textvariable=self.acc_calc[col][state],
                    width=12,
                    justify=CENTER,
                    state=DISABLED,
                ).grid(row=i, column=2, padx=10, pady=5, sticky=W)

                # Red Green Light
                self.canva[col][state] = Canvas(
                    frame_acc,
                    width=int(1 / 40 * screen_size["w_screen"]),
                    height=int(1 / 24 * screen_size["h_screen"]),
                )
                self.canva[col][state].grid(row=i, column=3, pady=5, sticky=W)
                self.canva[col][state].create_oval(
                    int(1 / 320 * screen_size["w_screen"]),
                    int(1 / 192 * screen_size["h_screen"]),
                    int(7 / 320 * screen_size["w_screen"]),
                    int(7 / 192 * screen_size["h_screen"]),
                )
                self.canva[col][state].addtag_withtag("circle", 1)

                pass_fail = (
                    "#93D976"
                    if abs(int(accuracy[col][state]) - calc_accuracy[col][state])
                    < int(accuracy[col][state]) * float(self.set_set["Tolerance"]["Percentage"])
                    else "#fa6464"
                )
                self.canva[col][state].itemconfig("circle", fill=pass_fail)

                i += 1
        Button(
            frame_button,
            text="Done",
            font=self.set_names["Font"]["M"],
            height=3,
            width=23,
            command=lambda: self.destroy(),
        ).grid(row=0, column=0, sticky=E)
