import json
from tkinter import *
from Numpad import Numpad

class InputBox():

    """
    Toplevel for InputBox Widget
    Parameters
    ----------
    text : str
        Text associated with the Label in previous root.
    Wscreen : str
        Providing Screen Size (Width) to Class.
    Hscreen : str
        Providing Screen Size (Height) to Class.
    """

    def __init__(self,text,Wscreen,Hscreen):

        with open('settings.json') as f:
            setData = json.load(f)
            self.font = setData['font']['L']

        self.root = Toplevel()
        self.text = text
        self.root.geometry(f"{int(Wscreen*0.5)}x{int(Hscreen*0.17)}+{int(Wscreen*0.1)}+20")
        self.root.title(f"Please Key in Input Quantity for {text}")
        self.root.columnconfigure(0,weight=1)
        self.root.columnconfigure(4,weight=1)
        self.inputVal = StringVar(self.root)
        self.window()
        self.num = Numpad(self.entry,Wscreen,Hscreen)
        self.root.mainloop()

    def window(self):        
        # Create Label, Entry and Button
        Label(self.root,text=f"Input Quantity for {self.text}",font=self.font).grid(row=0,column=1,pady=20,padx=7,sticky=W)
        self.entry = Entry(self.root,textvariable=self.inputVal,font=self.font)
        self.entry.grid(row=0,column=2,columnspan=2,pady=20,padx=7)
        Button(self.root, text="Submit",width=7,font=self.font,command=lambda: self.saveChange()).grid(row=1,column=3,pady=5,padx=3)
        
    def saveChange(self):
        # Destroy both Numpad and InputBox's Toplevel root
        self.num.root.destroy()
        self.root.quit()
        self.root.destroy()