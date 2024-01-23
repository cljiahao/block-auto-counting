from tkinter import Toplevel, Frame, Label, Entry
from tkinter import BOTH, NS, EW


class StaticNames(Toplevel):
    def __init__(self, root):
        Toplevel.__init__(self)
        self.initialize(root)

    def initialize(self, root):
        self.set_names = root.set_names
        self.set_colors = root.set_colors
        self.set_set = root.set_set

    def win_config(self):
        self.title("Static Name Config")
        self.frame = Frame(self)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self):
        pass
