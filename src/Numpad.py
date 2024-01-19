from tkinter import *

class Numpad():

    """
    Toplevel for Numpad Widget
    Parameters
    ----------
    entry : Tkinter.Entry
        For Entry Callback and inserting/deleting entry.
    Wscreen : str
        Providing Screen Size (Width) to Class.
    Hscreen : str
        Providing Screen Size (Height) to Class.
    """

    def __init__(self,entry,Wscreen,Hscreen):
        self.root = Toplevel()
        self.entry = entry
        self.root.geometry(f"{int(Wscreen*0.17)}x{int(Hscreen*0.4)}+{int(Wscreen*0.75)}+20")
        self.WBut = int(Wscreen * 0.005)
        self.HBut = int(Hscreen * 0.005)
        self.windows()
        
    def windows(self):
        
        # Create Buttons 1-9 in a 3x3 Mat
        j=0
        for i in range(9):
            if i%3 == 0 and i !=0:
                j+=1
            k = i%3
            Button(self.root,text=i+1,width=self.WBut,height=self.HBut,command=lambda p = i+1: self.entry.insert(END,p)).grid(row=j,column=k,padx=10,pady=7)
    
        # Create "0" Button
        Button(self.root,text=0,width=self.WBut*2,height=self.HBut,command=lambda: self.entry.insert(END,0)).grid(row=4,column=0,columnspan=2,pady=5)
        # Create "Del" Button
        Button(self.root,text="Del",width=self.WBut,height=self.HBut,command=lambda: self.entry.delete(self.entry.index("end") - 1)).grid(row=4,column=2,pady=5)

    