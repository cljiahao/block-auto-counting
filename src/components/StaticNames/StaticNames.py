from tkinter import Button, LabelFrame, Toplevel, Frame, Label
from tkinter import BOTH, NS, EW, E, W

from pages.Settings.components.scroll_cont import scroll_cont


class StaticNames(Toplevel):
    """
    StaticNames Window Component

    Parameters
    ----------
    root: root
        Parent root
    """

    def __init__(self, root):
        Toplevel.__init__(self)
        self.initialize(root)
        self.win_config()
        self.widgets()
        self.grab_set()

    def initialize(self, root):
        """Initialize variables"""
        self.set_names = root.set_names

    def win_config(self):
        """Tkinter Window Config"""
        self.title("Static Name Config")
        self.geometry("+800+50")
        self.frame = Frame(self)
        self.frame.columnconfigure(0, weight=1)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self):
        """Tkinter Widgets building"""
        s_font = self.set_names["Font"]["S"]
        m_font = self.set_names["Font"]["M"]

        # LABELFRAME: Frame for holding Scroll Container
        frame_main = LabelFrame(self.frame)
        frame_main.columnconfigure(0, weight=1)
        frame_main.columnconfigure(1, weight=1)
        frame_main.columnconfigure(2, weight=1)
        frame_main.grid(row=0, column=0)

        # Scrollbar container
        frame_def_stick = scroll_cont(frame_main, "7c")

        # Chip - Colour : Defect Mode
        def_stick_entry = {}
        i = 1
        for chip, value in self.set_names["Defect Sticker"].items():
            # Chip Label
            Label(frame_def_stick, text=f"GJM {chip}", font=m_font).grid(
                row=i, column=0, padx=5, pady=5, sticky=W
            )
            if chip not in def_stick_entry:
                def_stick_entry[chip] = {}
            i += 1
            for val in value.items():
                for j, v in enumerate(val):
                    # Return Colour and Mode
                    Label(frame_def_stick, text=v, font=s_font, relief="groove").grid(
                        row=i,
                        column=j + 1,
                        ipadx=15,
                        ipady=4,
                        padx=5,
                        pady=2,
                        sticky=EW,
                    )
                i += 1

        # FRAME: Frame for buttons
        frame_buttons = Frame(self.frame)
        frame_buttons.columnconfigure(0, weight=1)
        frame_buttons.grid(row=1, column=0, padx=5, pady=5, sticky=NS + EW)

        # Cancel Button
        Button(
            frame_buttons, text="Cancel", font=m_font, command=lambda: self.destroy()
        ).grid(row=0, column=0, padx=10, pady=10, sticky=NS + EW)
