from tkinter import *

from .NumPad import Numpad
from Utils.readSettings import readSettings

class InputBox(readSettings):
    def __init__(self,root,text,Wscreen,Hscreen):
        super().__init__()
        self.root = Toplevel(root)
        self.initialize()
        self.win_config(text,Wscreen,Hscreen)
        self.widget(text)
        self.num = Numpad(self.root,self.entry,Wscreen,Hscreen)
        self.root.grab_set()

    def initialize(self):
        self.inputVal = StringVar(self.root)

    def win_config(self,text,Wscreen,Hscreen):
        self.root.geometry(f"{int(Wscreen*0.5)}x{int(Hscreen*0.17)}+{int(Wscreen*0.1)}+20")
        self.root.title(f"Please Key in Input Quantity for {text}")
        self.root.columnconfigure(0,weight=1)
        self.root.columnconfigure(4,weight=1)

    def widget(self,text):    
        # Create Label, Entry and Button
        Label(self.root,text=f"Input Quantity for {text}",font=self.font['L']).grid(row=0,column=1,pady=20,padx=7,sticky=W)
        self.entry = Entry(self.root,textvariable=self.inputVal,font=self.font['L'])
        self.entry.grid(row=0,column=2,columnspan=2,pady=20,padx=7)
        Button(self.root, text="Submit",width=7,font=self.font['L'],command=lambda: self.saveChange()).grid(row=1,column=3,pady=5,padx=3)
        
    def saveChange(self):
        # Destroy both Numpad and InputBox's Toplevel root
        self.root.destroy()