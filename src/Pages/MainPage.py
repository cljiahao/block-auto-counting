import os
import cv2
import time
import requests
from tkinter import *
from datetime import datetime
from tkinter import messagebox
from PIL import Image as PilImg, ImageTk

from Components.Login import Login
from Components.InputBox import InputBox
from Components.Lighting import Lighting
from Pages.Accuracy import Accuracy
from Pages.Summary import Summary
from Utils.saveExcel import Excel
from Utils.readSettings import readSettings
from Utils.imgProcess import Process

class MainWindow(readSettings):
    def __init__(self,root):
        super().__init__()
        self.root = root
        self.light = Lighting()
        if not self.config['Trouble']: self.light.initialize()
        self.defVar = {}
        self.camera()
        self.win_config()
        self.widgets()

    def camera(self):
        self.cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,int(self.config['CamResWidth']))
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,int(self.config['CamResHeight']))

    def win_config(self):
        self.root.state('zoomed')
        self.root.title('Block Cutting Automation')
        self.Hscreen = self.root.winfo_screenheight()
        self.Wscreen = self.root.winfo_screenwidth()
        self.frame = Frame(self.root)
        self.frame.columnconfigure(0,weight=1)
        self.frame.rowconfigure(len(self.defCode),weight=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.reg = (self.root.register(self.callback),'%P','%W')

    def widgets(self):
        # Image captured to be displayed in this container
        self.capture = Label(self.frame, relief=SUNKEN)
        self.capture.grid(row=0, column=0, rowspan=len(self.defCode)+5, columnspan=2, padx=5, pady=10, sticky=NS+EW)

        # Frame to hold the defect modes containers
        ####################################################################################################
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

            if j%2 == 0: k = 3
            else:
                k = 0
                l += 1
            
        # Lot Number Scan In
        #################################################################################################### 
        lotMcFrame = LabelFrame(self.frame, bd=3, relief=FLAT)
        lotMcFrame.grid(row=len(self.defCode)+1, column=2, columnspan=2, sticky=EW)
        lotMcFrame.columnconfigure(3,weight=1)

        entrytxt = ["Lot Number","M/C Number","PayRoll Number","Input Quantity"]

        for i, entxt in enumerate(entrytxt):
            Label(lotMcFrame, text=entxt, wraplength=50, justify=LEFT).grid(row=i%2, column=0 if i<2 else 4, pady=5, padx=3, sticky=W)

        self.lotNumberEdit = Entry(lotMcFrame, name="lotno", font=self.font['L'], width=11, justify=CENTER, validate="key", validatecommand=self.reg)
        self.lotNumberEdit.grid(row=0, column=1, columnspan=2, pady=3, sticky=E)

        self.payRollEdit = Entry(lotMcFrame, name="payroll", font=self.font['L'], width=11, justify=CENTER, validate="key", validatecommand=self.reg)
        self.payRollEdit.grid(row=0, column=5, columnspan=2, pady=3, sticky=E)

        self.mcNumberEdit = Entry(lotMcFrame, name="mcno", font=self.font['L'], width=11, justify=CENTER, validate="key", validatecommand=self.reg)
        self.mcNumberEdit.grid(row=1, column=1, columnspan=2, pady=3, sticky=E)

        self.inQtyEdit = Entry(lotMcFrame, name="inqty", font=self.font['L'], width=11, justify=CENTER, validate="key", validatecommand=self.reg)
        self.inQtyEdit.grid(row=1, column=5, columnspan=2, pady=3, sticky=E)

        # Spinner for Item Drop Down (02, 03 or 15)
        ####################################################################################################
        AccNChipFrame = LabelFrame(self.frame, bd=3, relief=FLAT)
        AccNChipFrame.grid(row=len(self.defCode)+3, column=2, columnspan=2, sticky=EW)
        AccNChipFrame.columnconfigure(3,weight=1)

        self.chipType = Label(AccNChipFrame, text="ChipType", font=self.font['L'], bg='#ecedcc')
        self.chipType.grid(row=0,column=1,columnspan=3,padx=(0,10),pady=5)

        accSel = StringVar(value=list(self.accuracy.keys())[0])
        self.accdrop = OptionMenu(AccNChipFrame,accSel,*self.accuracy)
        self.accdrop.config(width=int(self.Wscreen*0.015),height=int(self.Hscreen*0.0027),font=self.font['M'],anchor=CENTER,bg="#c6e2e9")
        self.accdrop.grid(row=0,column=4,columnspan=3,padx=(0,10),pady=5)

        accSel.trace('w',self.colorCB)

        # Buttons
        ####################################################################################################
        buttonFrame = LabelFrame(self.frame, bd=3, relief=FLAT)
        buttonFrame.grid(row=len(self.defCode)+4, column=2, columnspan=6, sticky=EW)

        summary = Button(buttonFrame, text="Summary", height=2, width=15, command=lambda: self.showSum(True))
        summary.grid(row=0, column=0, padx=5, pady=3, sticky=S)

        accuracy = Button(buttonFrame, text="Accuracy", height=2, width=15, command=lambda: Accuracy(self.root,self.prepCam(),accSel.get(),self.Wscreen,self.Hscreen))
        accuracy.grid(row=0,column=1, padx=5, pady=3, sticky=S)

        settings = Button(buttonFrame, text="Settings", height=2, width=15, command=lambda: Login(self.root,self.cap,self.Wscreen,self.Hscreen,self.light,accSel.get()))
        settings.grid(row=0, column=2, padx=5, pady=3, sticky=S)

        snap = Button(buttonFrame, text="Snap", height=2, width=35, font='sans 15 bold', bg="#ecedcc", command=lambda: self.processImg(self.chipType.cget('text')[-2:],accSel.get()))
        snap.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=EW + S)

    ####################################################################################################
    """
    Functions Used for the Widgets Above
    """ 
    ####################################################################################################


    def colorCB(self,name,index,mode):
        if self.root.getvar(name) == "EQA": self.accdrop.config(bg="#c6e2e9") 
        elif self.root.getvar(name) == "DMA": self.accdrop.config(bg="#fffdaf")
        else: self.accdrop.config(bg="#c7ceea")

    # Checking Entry Boxes and Focus when criteria matches
    ####################################################################################################
    def callback(self,input,name):
        if name.split(".")[-1] == "lotno":
            if len(input) == 10:
                self.inputRetrieve(input)
                foldir = os.path.join(self.dataPath,datetime.today().strftime("%b%y"))
                if not os.path.exists(foldir): os.makedirs(foldir)
                self.filePath = os.path.join(foldir,input+".xlsx")
                self.payRollEdit.focus()
        elif name.split(".")[-1] == "payroll" and len(input) == 7: self.mcNumberEdit.focus()
        elif name.split(".")[-1] == "mcno" and len(input) == 3: self.inQtyEdit.focus()
        return True

    # Retrieve Lot number from entry and retrieve Input Quantity
    ####################################################################################################
    def inputRetrieve(self,lotNum):
        url = self.address['QtyWeb']+lotNum
        res = requests.get(url)
        if res.status_code == 200:
            self.inQtyEdit.delete(0,END)
            self.inQtyEdit.insert(0,res.json()['sun0011'])
            chipCode = ["Error!","#fa6464"] if res.json()['cdc0163'] == None else [res.json()['cdc0163'][:5],"#a6eca8"]
            self.chipType.config(text=chipCode[0],bg=chipCode[1])
        else: messagebox.showerror("Lot not Found in Database","Lot not Found in Database")

    # Check for correct input before proceeding to processing image captured
    ####################################################################################################
    def chkEntry(self,var):

        errCode = {
            'lotError' : {'title':'Lot Number Not Found', 'message':'Please Input the Lot No'},
            'payError' : {'title':'Payroll Not Found', 'message':'Please Input the Payroll No'},
            'mcError' : {'title':'Machine Number Not Found', 'message':'Please Input the Machine No'},
            'inputError' : {'title':'Input Quantity Not Found', 'message':'Please Input the Input Quantity'}
        }
        if len(self.lotNumberEdit.get()) != 10: return messagebox.showerror(**errCode['lotError']) != "ok"
        if var:
            if len(self.payRollEdit.get()) == 0: return messagebox.showerror(**errCode['payError']) != "ok"
            elif len(self.mcNumberEdit.get()) == 0: return messagebox.showerror(**errCode['mcError']) != "ok"
            elif len(self.inQtyEdit.get()) == 0: return messagebox.showerror(**errCode['inputError']) != "ok"
        return True

    # For Editing Entry Box (E.g Sample and Drop Chip) input by User
    ####################################################################################################
    def SamDropInput(self,text):
        if self.chkEntry(False):
            inputValue = InputBox(self.root,text,self.Wscreen,self.Hscreen).inputVal.get()
            if inputValue == "": inputValue = 0
            self.defVar[text].config(text=inputValue)
            Excel(self.filePath,self.defVar,text)
    
    # Preparing Camera for image to process
    ####################################################################################################
    def prepCam(self):
        imgArr = []
        if self.config['Trouble']:
            imgArr.extend(["","",""])
            imgfile = os.path.join(self.troublePath,datetime.today().strftime("%d-%m-%y")+".png")
            imgArr.append(cv2.imread(imgfile))
        else:
            self.light.lightingOn()
            self.cap.release()                      # Takes 0.5 seconds to release
            self.camera()                           # Takes 1.5 seconds to start up videocapture
            for i in range(13):                     # Takes 0.1 seconds to snap each shot per cycle range
                image = self.cap.read()[1]
                imgArr.append(image[:,int(int(self.config['CamResWidth'])/6):int(int(self.config['CamResWidth'])/6*5)])
            self.light.lightingOff()
            
        return imgArr[3:]

    # Process image and show to User
    ####################################################################################################
    def processImg(self,chip,mat):
        if self.config['Trouble']: chip = '03'
        for defName in self.defCode: self.defVar[defName].config(text="0")
        if self.chkEntry(True):
            try:
                imgArr = self.prepCam()
                baseimg, image, Defects = Process(self.root,imgArr,False,self.Wscreen,self.Hscreen,chip,mat).res
                self.saveImg(baseimg,"block",self.lotNumberEdit.get()+"_"+datetime.today().strftime("%d-%m-%y_%H%M%S"))
                img = PilImg.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
                img = img.resize((int(img.size[0]*0.75),int(img.size[1]*0.75)))
                imgtk = ImageTk.PhotoImage(image = img)
                self.capture.imgtk = imgtk
                self.capture.config(image = imgtk)

                for defappend in self.defVar:
                    if defappend == "DROPCHIP" or defappend == "SAMPLE":
                        addition = int(self.defVar[defappend].cget("text")) + Defects[defappend]
                        self.defVar[defappend].config(text=str(addition))
                    else: self.defVar[defappend].config(text=Defects[defappend])

                Excel(self.filePath,self.defVar)
                cv2.destroyAllWindows()
            except Exception as e: 
                print(e)
                self.light.lightingOff()

    # Open Summary Window to show Summary of Processed Images
    ####################################################################################################
    def showSum(self,res):
        if self.chkEntry(False) and res:
            inData = [self.lotNumberEdit.get(),self.mcNumberEdit.get(),self.payRollEdit.get(),self.inQtyEdit.get()]
            self.showSum(Summary(self.root,inData,self.filePath,self.Wscreen,self.Hscreen).res)
        else: self.reset()

    # Reset User Interface for new / next process
    ####################################################################################################
    def reset(self):
        self.lotNumberEdit.delete(0,END)
        self.mcNumberEdit.delete(0,END)
        self.payRollEdit.delete(0,END)
        self.inQtyEdit.delete(0,END)
        self.lotNumberEdit.focus()
        self.capture.config(image = "")
        self.chipType.config(text="ChipType",bg="#ecedcc")
        for defName in self.defCode: self.defVar[defName].config(text="0")

    # Saving Images 
    ####################################################################################################
    def saveImg(self,img,loc,timestp):
        if not self.config['Trouble']:
            imgdir = os.path.join(self.basePath,loc,datetime.today().strftime("%b%y"))
            if not os.path.exists(imgdir): os.makedirs(imgdir)
            imgfile = os.path.join(imgdir,timestp+".png")
            if not os.path.exists(imgfile): cv2.imwrite(imgfile,img)
