from tkinter import Toplevel, Button
from tkinter import END


class Numpad(Toplevel):
    """
    Tkinter Component with One Entry Box
    Parameters
    ----------
    parent : root
        The parent root.
    screen_size : dict
        Providing Screen Size (Width and Height) to Class.
    entry : Tkinter Component
        Reference to Entry Box.
    """

    def __init__(self, parent, screen_size, entry):
        Toplevel.__init__(self, parent)
        self.win_config(screen_size)
        self.widgets(entry)

    def win_config(self, screen_size):
        self.geometry(
            f"{int(screen_size['w_screen']*0.17)}x{int(screen_size['h_screen']*0.4)}+{int(screen_size['w_screen']*0.75)}+20"
        )
        self.but_width = int(screen_size["w_screen"] * 0.005)
        self.but_height = int(screen_size["h_screen"] * 0.005)

    def widgets(self, entry):
        # Create Buttons 1-9 in a 3x3 Mat
        j = 0
        for i in range(9):
            if i % 3 == 0 and i != 0:
                j += 1
            k = i % 3
            Button(
                self,
                text=i + 1,
                width=self.but_width,
                height=self.but_height,
                command=lambda p=i + 1: entry.insert(END, p),
            ).grid(row=j, column=k, padx=10, pady=7)

        # Create "0" Button
        Button(
            self,
            text=0,
            width=self.but_width,
            height=self.but_height,
            command=lambda: entry.insert(END, 0),
        ).grid(row=4, column=0, pady=5)
        # Create "." Button
        Button(
            self,
            text=".",
            width=self.but_width,
            height=self.but_height,
            command=lambda: entry.insert(END, "."),
        ).grid(row=4, column=1, pady=5)
        # Create "Del" Button
        Button(
            self,
            text="Del",
            width=self.but_width,
            height=self.but_height,
            command=lambda: entry.delete(entry.index("end") - 1),
        ).grid(row=4, column=2, pady=5)
