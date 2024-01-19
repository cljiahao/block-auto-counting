import os
import cv2
import time
import json
import requests
from tkinter import *
from datetime import date
from tkinter import messagebox
from PIL import Image as PilImg, ImageTk

from Login import *
from Summary import *
from Accuracy import *
from InputBox import *
from Processing import *
from LightingCont import *

class MainWindow:

    
    def __init__(self):
        super().__init__()

        with open('settings.json') as f:
            setData = json.load(f)
            self.defCode = setData['staticName']['defCode']
            misc = setData['Misc']
            self.sleep = misc['Sleep']
            self.trouble = misc['Trouble']
            self.font = setData['font']['normal']
            self.chip = setData['Chip Size']
            self.acc = setData['Accuracy']
            self.camW = int(misc['CamResWidth'])
            self.camH = int(misc['CamResHeight'])
            
        self.root = Tk()
        self.root.state("zoomed")
        self.root.title("Block Cutting Automation")
        self.Hscreen = self.root.winfo_screenheight()
        self.Wscreen = self.root.winfo_screenwidth()
        self.frame = Frame(self.root)
        self.frame.columnconfigure(0,weight=1)
        self.frame.rowconfigure(len(self.defCode),weight=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,self.camW)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,self.camH)
        self.defVar = {}
        self.reg = (self.root.register(self.callback),'%P','%W')
        self.windows()
        self.root.mainloop() 

    def windows(self):
        # Image captured to be displayed in this container
        self.capture = Label(self.frame, relief=SUNKEN)
        self.capture.grid(row=0, column=0, rowspan=len(self.defCode)+5, columnspan=2, padx=5, pady=10, sticky=NS+EW)

        # Frame to hold the defect modes containers
        defectsInfo = LabelFrame(self.frame, bd=5, relief=FLAT)
        defectsInfo.grid(row=0, column=2, columnspan=2, pady=7, sticky=EW)
        
        # Create Label for Defect Code, Defect Name, Defect Quantity based from Naming.py
        k, l = 0, 0
        for j, defName in enumerate(self.defCode):

            if defName == "DROPCHIP" or defName == "SAMPLE":
                Label(defectsInfo, text=f"[{self.defCode[defName]}]").grid(row=l, column=k, padx=7, pady=5, sticky=W)
                Button(defectsInfo, text=defName, command=lambda defName=defName: self.SamDropInput(defName)).grid(row=l, column=k+1, pady=5, sticky=W)
                self.defVar[defName] = Label(defectsInfo, text="0", width=10, relief=RIDGE)
                self.defVar[defName].grid(row=l, column=k+2, pady=5, sticky=W)

            else:
                Label(defectsInfo, text=f"[{self.defCode[defName]}]").grid(row=l, column=k, padx=7, pady=5, sticky=W)
                Label(defectsInfo, text=defName).grid(row=l, column=k+1, pady=5, sticky=W)
                self.defVar[defName] = Label(defectsInfo, text="0", width=10, relief=RIDGE)
                self.defVar[defName].grid(row=l, column=k+2, pady=5, sticky=W)

            if j%2 == 0:
                k = 3
            else:
                k = 0
                l += 1
            
    
        # Lot Number Scan In
        #######################################################################################
        
        lotMcFrame = LabelFrame(self.frame, bd=3, relief=FLAT)
        lotMcFrame.grid(row=len(self.defCode)+1, column=2, columnspan=2, sticky=EW)
        lotMcFrame.columnconfigure(3,weight=1)

        entrytxt = ["Lot Number","M/C Number","PayRoll Number","Input Quantity"]

        for i, entxt in enumerate(entrytxt):
            Label(lotMcFrame, text=entxt, wraplength=50, justify=LEFT).grid(row=i%2, column=0 if i<2 else 4, pady=5, padx=3, sticky=W)

        self.lotNumberEdit = Entry(lotMcFrame, name="lotno", font=("Courier", 15), width=11, justify=CENTER, validate="key", validatecommand=self.reg)
        self.lotNumberEdit.grid(row=0, column=1, columnspan=2, pady=3, sticky=E)

        self.payRollEdit = Entry(lotMcFrame, name="payroll", font=("Courier", 15), width=11, justify=CENTER, validate="key", validatecommand=self.reg)
        self.payRollEdit.grid(row=0, column=5, columnspan=2, pady=3, sticky=E)

        self.mcNumberEdit = Entry(lotMcFrame, name="mcno", font=("Courier", 15), width=11, justify=CENTER, validate="key", validatecommand=self.reg)
        self.mcNumberEdit.grid(row=1, column=1, columnspan=2, pady=3, sticky=E)

        self.inQtyEdit = Entry(lotMcFrame, name="inqty", font=("Courier", 15), width=11, justify=CENTER, validate="key", validatecommand=self.reg)
        self.inQtyEdit.grid(row=1, column=5, columnspan=2, pady=3, sticky=E)

        # Spinner for Item Drop Down (02, 03 or 15)
        #######################################################################################

        AccNChipFrame = LabelFrame(self.frame, bd=3, relief=FLAT)
        AccNChipFrame.grid(row=len(self.defCode)+3, column=2, columnspan=2, sticky=EW)
        AccNChipFrame.columnconfigure(3,weight=1)

        self.chipSel = StringVar(value=list(self.chip.keys())[0])
        chipdrop = OptionMenu(AccNChipFrame,self.chipSel,*self.chip)
        chipdrop.config(width=int(self.Wscreen*0.015),height=int(self.Hscreen*0.0025),anchor=CENTER)
        chipdrop.grid(row=0,column=1,columnspan=3,padx=(0,10),pady=5)
        self.accSel = StringVar(value=list(self.acc.keys())[0])
        accdrop = OptionMenu(AccNChipFrame,self.accSel,*self.acc)
        accdrop.config(width=int(self.Wscreen*0.015),height=int(self.Hscreen*0.0025),anchor=CENTER)
        accdrop.grid(row=0,column=4,columnspan=3,padx=(0,10),pady=5)

        # Buttons
        #######################################################################################

        buttonFrame = LabelFrame(self.frame, bd=3, relief=FLAT)
        buttonFrame.grid(row=len(self.defCode)+4, column=2, columnspan=6, sticky=EW)

        summary = Button(buttonFrame, text="Summary", height=2, width=15, command=lambda: self.showSum())
        summary.grid(row=0, column=0, padx=5, pady=3, sticky=S)

        accuracy = Button(buttonFrame, text="Accuracy", height=2, width=15, command=lambda: Accuracy(self.prepCam(),self.accSel.get(),self.chipSel.get(),self.Wscreen,self.Hscreen))
        accuracy.grid(row=0,column=1, padx=5, pady=3, sticky=S)

        settings = Button(buttonFrame, text="Settings", height=2, width=15, command=lambda: Login(self.cap,self.Wscreen,self.Hscreen))
        settings.grid(row=0, column=2, padx=5, pady=3, sticky=S)

        snap = Button(buttonFrame, text="Snap", height=2, width=35, font='sans 15 bold', bg="#ecedcc", command=lambda: self.show_frames())
        snap.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=EW + S)

    # Checking Entry Boxes and Focus when criteria matches
    #######################################################################################
    def callback(self,input,name):
        if name.split(".")[-1] == "lotno":
            if len(input) == 10:
                self.inputRetrieve(input)
                foldir = os.path.join(os.path.dirname(os.path.dirname(__file__)),"data",datetime.today().strftime("%b%y"))
                if not os.path.exists(foldir): os.makedirs(foldir)
                self.filepath = os.path.join(foldir,input+".xlsx")
                self.payRollEdit.focus()
        elif name.split(".")[-1] == "payroll":
            if len(input) == 7:
                self.mcNumberEdit.focus()
        elif name.split(".")[-1] == "mcno":
            if len(input) == 3:
                self.inQtyEdit.focus()
        return True

    # Retrieve Lot number from entry and retrieve Input Quantity
    #######################################################################################
    def inputRetrieve(self,lotNum):
        url = config['QtyWeb']+lotNum
        res = requests.get(url)
        if res.status_code == 200:
            self.inQtyEdit.delete(0,END)
            self.inQtyEdit.insert(0,res.json()['sun0011'])
        return True
    
    def save_Data(self):

        if os.path.exists(self.filepath):
            wb = load_workbook(self.filepath)
            newCol = wb.active.max_column + 1
            
            for i, defs in enumerate(self.defVar):
                wb.active.cell(row=i+1,column=newCol).value = self.defVar[defs].cget("text")

        else:
            wb = Workbook()

            for i, defs in enumerate(self.defVar):
                wb.active.cell(row=i+1,column=1).value = defs
                wb.active.cell(row=i+1,column=2).value = self.defVar[defs].cget("text")

        wb.save(self.filepath)

    def SamDropInput(self,text):
        
        if self.chkEntry(False):

            inputValue = InputBox(text,self.Wscreen,self.Hscreen)
            self.defVar[text].config(text=inputValue.inputVal.get())   

            if os.path.exists(self.filepath):
                wb = load_workbook(self.filepath)
                maxcol = wb.active.max_column

                for r in wb.active.iter_rows(max_row=wb.active.max_row,max_col=1):
                    for c in r:
                        if c.value == text:
                            if maxcol == 1:
                                maxcol += 1
                            wb.active.cell(row=c.row,column=maxcol).value = self.defVar[text].cget("text")
            
            else:
                wb = Workbook()

                for i, defs in enumerate(self.defVar):
                    wb.active.cell(row=i+1,column=1).value = defs
                    wb.active.cell(row=i+1,column=2).value = self.defVar[defs].cget("text")
            
            wb.save(self.filepath)
    
    def chkEntry(self,var):

        if len(self.lotNumberEdit.get()) != 10:
            messagebox.showerror("Lot Number Not Found", "Please Input the Lot No")
            return False
        else:
            if var:
                if len(self.payRollEdit.get()) == 0:
                    messagebox.showerror("Payroll Not Found", "Please Input the Payroll No")
                    return False
                elif len(self.mcNumberEdit.get()) == 0:
                    messagebox.showerror("M/C No Not Found", "Please Input the Machine No")
                    return False
                elif len(self.inQtyEdit.get()) == 0:
                    messagebox.showerror("Input Quantity Not Found", "Please Input the Input Quantity")
                    return False
                else:
                    return True
            else:
                return True

    def prepCam(self):
        start = time.time()
        lightingOn()
        print("Light End: ",time.time()-start)
        time.sleep(int(self.sleep))
        start = time.time()
        self.cap.release()
        print("Release End: ",time.time()-start)
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,self.camW)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,self.camH)
        if self.trouble:
            imgfile = os.path.join(os.path.dirname(os.path.dirname(__file__)),"temp",date.today().strftime("%d-%m-%y")+".png")
            image = cv2.imread(imgfile)
        else:
            image = self.cap.read()[1]
            image = image[:,int(self.camW/6):int(self.camW/6*5)]
        return image

    def show_frames(self):
        if self.chkEntry(True):
            image = self.prepCam()
            image, Defects = Capture(image,self.chipSel.get(),self.lotNumberEdit.get(),self.Wscreen,self.Hscreen)
            img = PilImg.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
            img = img.resize((int(img.size[0]*0.75),int(img.size[1]*0.75)))
            imgtk = ImageTk.PhotoImage(image = img)
            self.capture.imgtk = imgtk
            self.capture.config(image = imgtk)
            lightingOff()

            for defappend in self.defVar:
                if defappend == "DROPCHIP" or defappend == "SAMPLE":
                    addition = int(self.defVar[defappend].cget("text")) + Defects[defappend]
                    self.defVar[defappend].config(text=str(addition))
                else:
                    self.defVar[defappend].config(text=Defects[defappend])

            self.save_Data()
            cv2.destroyAllWindows()

    def showSum(self):
        res = Summary(self.lotNumberEdit.get(),self.mcNumberEdit.get(),
        self.payRollEdit.get(),self.inQtyEdit.get(),self.Wscreen,self.Hscreen,self.filepath).res
        if res:
            self.reset()

    def reset(self):
        self.lotNumberEdit.delete(0,END)
        self.mcNumberEdit.delete(0,END)
        self.payRollEdit.delete(0,END)
        self.inQtyEdit.delete(0,END)
        self.lotNumberEdit.focus()
        self.capture.config(image = "")
        for defName in self.defCode:
            self.defVar[defName].config(text="0")
        
