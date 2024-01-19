import cv2
import json
from tkinter import *
from tkinter import messagebox
from PIL import Image as PilImg, ImageTk

class OddStick_Window(object):
    def __init__(self,Pieces,Bimg,Wscreen,Hscreen):

        with open('settings.json') as f:
            setData = json.load(f)
            self.font = setData['font']['normal']
            self.TexCol = setData['Highlight']
            self.defCode = setData['staticName']['defCode']
            self.blkdefCode = setData['staticName']['defCode']  # <<< Change this from defCode to black_Def in the future

        self.Pieces = Pieces
        self.Wscreen,self.Hscreen = Wscreen,Hscreen
        img = PilImg.fromarray(cv2.cvtColor(Bimg,cv2.COLOR_BGR2RGB))
        img = img.resize((int(img.size[0]*0.75),int(img.size[1]*0.75)))
        self.imgtk = ImageTk.PhotoImage(image = img)
        self.choose1 = "Choose 1"
        self.root = Toplevel()
        self.root.title("Black Sticker Window")
        self.root.geometry(f"{int(self.Wscreen*0.7)}x{int(self.Hscreen*0.9)}+30+10")
        self.frame = Frame(self.root)
        self.frame.columnconfigure(0,weight=1)
        self.frame.rowconfigure(9,weight=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.frameHold, self.dropbox, self.config, self.selected ={},{},{},{}
        self.window()
        self.root.grab_set()
        self.root.mainloop()

    def window(self):
        # Image captured to be displayed in this container
        self.imgWin = Label(self.frame, relief=SUNKEN, image=self.imgtk)
        self.imgWin.grid(row=0, column=0, rowspan=19, columnspan=2, padx=5, pady=10, sticky=NS+EW)

        # Button to Save Selection and return Black Sticker Defects
        btn_OddStick = Button(self.frame, text="Save Changes", font=self.font, height=2, width=15, command=lambda: self.saveSelected())
        btn_OddStick.grid(row=10, column=len(self.Pieces)*2, columnspan=2, pady=20, padx=10, sticky=NE)     
        
        # Set up Black Sticker layout but not injected into Tkinter yet
        ##################################################################################################
        i = 1
        for key, value in self.Pieces.items():
            if key in self.TexCol.keys():
                self.frameHold[key] = LabelFrame(self.frame,bd=5,relief=FLAT,text=key)
                self.frameHold[key].grid(row=0, column=2*i, columnspan=2, ipadx=5, padx=5, pady=7, sticky=E)
                i+=1
                self.dropbox[key], self.config[key] = {}, {}
                for j in range(len(value)):
                    Label(self.frameHold[key], text=f"[{j+1}]").grid(row=j, column=0, pady=3, padx=10, sticky=W)
                    self.dropbox[key][j] = StringVar(self.frameHold[key])
                    self.dropbox[key][j].set(self.choose1)
                    if key.lower() == "black":
                        self.config[key][j] = OptionMenu(self.frameHold[key],self.dropbox[key][j],*self.blkdefCode)
                        self.config[key][j].config(width=13)
                        self.config[key][j].grid(row=j, column=1, pady=3, sticky=W)
                    else:
                        self.config[key][j] = OptionMenu(self.frameHold[key],self.dropbox[key][j],*self.defCode)
                        self.config[key][j].config(width=13)
                        self.config[key][j].grid(row=j, column=1, pady=3, sticky=W)

    def saveSelected(self):

        for key, value in self.Pieces.items():
            if key in self.TexCol.keys():
                self.selected[key] = {}
                for k in range(len(value)):
                    if self.dropbox[key][k].get() in self.selected[key].keys():
                        self.selected[key][self.dropbox[key][k].get()] += self.Pieces[key][k]
                    else:
                        self.selected[key][self.dropbox[key][k].get()] = self.Pieces[key][k]
            a = 0
        for ky in self.selected.keys():
            if not self.selected[ky] == {}:
                if "Choose 1" in self.selected[ky].keys():
                    if a == 0:
                        messagebox.showwarning("Empty Selection","Please Choose 1!",parent=self.root)
                        a+=1                
                else:
                    self.root.quit()