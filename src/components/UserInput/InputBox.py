from tkinter import Toplevel, StringVar, Label, Entry, Button
from tkinter import W

from components.UserInput.NumPad import Numpad


class InputBox(Toplevel):
    """
    Tkinter Component with One Entry Box
    Parameters
    ----------

    screen_size : dict
        Providing Screen Size (Width and Height) to Class.
    text : str
        Reference Name for Entry Box.
    """

    def __init__(self, settings, screen_size, text):
        Toplevel.__init__(self)
        self.initialize(settings)
        self.win_config(screen_size, text)
        self.widget(text)
        self.num = Numpad(self, screen_size, self.entry)
        self.grab_set()
        self.mainloop()

    def initialize(self, settings):
        self.set_name = settings["Names"]
        self.input_val = StringVar(self)

    def save_change(self):
        """Destroy both Numpad and InputBox's Toplevel root"""
        self.destroy()
        self.quit()

    def win_config(self, screen_size, text):
        self.geometry(
            f"{int(screen_size['w_screen']*0.5)}x{int(screen_size['h_screen']*0.17)}+{int(screen_size['w_screen']*0.1)}+20"
        )
        self.title(f"Please Key in Input Quantity for {text}")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(4, weight=1)

    def widget(self, text):
        """Create Label, Entry and Button"""
        # Label
        Label(
            self, text=f"Input Quantity for {text}", font=self.set_name["Font"]["L"]
        ).grid(row=0, column=1, pady=20, padx=7, sticky=W)
        # Entry Box
        self.entry = Entry(
            self, textvariable=self.input_val, font=self.set_name["Font"]["L"]
        )
        self.entry.grid(row=0, column=2, columnspan=2, pady=20, padx=7)
        # Submit Button
        Button(
            self,
            text="Submit",
            width=7,
            font=self.set_name["Font"]["L"],
            command=lambda: self.save_change(),
        ).grid(row=1, column=3, pady=5, padx=3)
