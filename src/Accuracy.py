from LightingCont import *
from Debug import *
from Processing import *

class Accuracy():

    """
    Used for Accuracy Checking before usage
    Parameters
    ----------
    Aimg : 3-D Image MAT
        Src input image
    acc : str
        Which acc block to work on
    chip : str
        Which chip size / type to work on
    Wscreen : str
        Providing Screen Size (Width) to Class.
    Hscreen : str
        Providing Screen Size (Height) to Class.
    """

    def __init__(self,Aimg,acc,chip,Wscreen,Hscreen):

        with open('settings.json') as f:
            setData = json.load(f)
            self.font = setData['font']['normal']
            accuracy = setData['Accuracy']
            self.Acc = accuracy[acc]
            self.tolerance = setData['Tolerance']
            self.ChipArea = float(setData['Chip Size'][chip]['L'])*float(setData['Chip Size'][chip]['W'])


        self.Aimg = Aimg
        self.chip = chip
        self.accName = acc
        self.root = Toplevel()
        self.root.title("Accuracy Check Window")
        self.Wscreen,self.Hscreen = Wscreen,Hscreen
        self.root.geometry(f"{int(Wscreen*0.73)}x{int(Hscreen*0.80)}+50+20")
        self.frame = Frame(self.root)
        self.frame.pack(fill=BOTH, expand=True)
        self.setAcc, self.AccVar, self.AccProc, self.Canva = {},{},{},{}
        self.process()
        lightingOff()
        self.window()
        self.update()
        self.root.grab_set()
        self.root.mainloop()

    def window(self):
        # Image captured to be displayed in this container
        self.imgWin = Label(self.frame, relief=SUNKEN, image=self.imgtk)
        self.imgWin.grid(row=0, column=0, rowspan=19, columnspan=2, padx=5, pady=10, sticky=NS+EW)

        AccFrame = LabelFrame(self.frame,bd=5,relief=FLAT)
        AccFrame.grid(row=0, column=3, columnspan=2, ipadx=5, padx=5, pady=7, sticky=E)

        ButFrame = LabelFrame(self.frame,bd=5,relief=FLAT)
        ButFrame.grid(row=18, column=3, columnspan=2, ipadx=5, padx=5, pady=7, sticky=E)

        i=0
        for col in self.Acc:
            for state in self.Acc[col]:
                setName = col+state
                self.setAcc[setName] = StringVar(AccFrame, value=self.Acc[col][state])
                Label(AccFrame, font=self.font, text=setName).grid(row=i, column=0, sticky=W, padx=10, pady=5)
                self.AccVar[setName] = Label(AccFrame, text="0", width=10, relief=RIDGE)
                self.AccVar[setName].grid(row=i, column=1, pady=5, sticky=W)
                Entry(AccFrame, font=self.font, textvariable=self.setAcc[setName], width=12, justify=CENTER).grid(row=i, column=2, sticky=W, padx=10, pady=5)
                self.Canva[setName] = Canvas(AccFrame,width=int(1/40*self.Wscreen),height=int(1/24*self.Hscreen))
                self.Canva[setName].grid(row=i, column=3, pady=5, sticky=W)
                self.Canva[setName].create_oval(int(1/320*self.Wscreen),int(1/192*self.Hscreen),int(7/320*self.Wscreen),int(7/192*self.Hscreen))
                self.Canva[setName].addtag_withtag("circle",1)
                i+=1

        btn_Close = Button(ButFrame, text="Done", font=self.font, height=3, width=23, command=lambda: self.root.destroy())
        btn_Close.grid(row = 0, column = 0, sticky = E)

    def process(self):

        saveImg(self.Aimg,"acclog",datetime.today().strftime("%d-%m-%y"))
        Proimg,cnts,avgPixLen,ChipArea,_ = mainPro(self.Aimg,self.chip)

        AProimg = Proimg.copy()
        timestp = datetime.today().strftime("%d-%m-%y_%H%M%S")

        blur = cv2.GaussianBlur(Proimg.copy(), (5, 5), 0)
        hsvimg = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV_FULL)

        for cnt in cnts:
            if 100000<cv2.contourArea(cnt) or cv2.contourArea(cnt)<30:
                continue

            cArea = cv2.contourArea(cnt)
            realsize = cArea*avgPixLen
            pieces = realsize/ChipArea
            length = round(math.sqrt(cArea*avgPixLen))

            _,hasCol = StickerColor(hsvimg, cnt)

            for colName in hasCol:
                if hasCol[colName] > 0:
                    if colName+"Chips" in self.AccProc.keys():
                        self.AccProc[colName+"Num"] += 1
                        self.AccProc[colName+"Chips"] += pieces
                    else:
                        self.AccProc[colName+"Num"] = 1
                        self.AccProc[colName+"Chips"] = pieces
                    AProimg = TextAdding(AProimg,cArea,cnt,pieces,True)
                    dataLog(self.accName,[timestp,avgPixLen,colName,cArea,realsize])
                else:
                    if colName+"Chips" in self.AccProc.keys():
                        self.AccProc[colName+"Num"] += 0
                        self.AccProc[colName+"Chips"] += 0
                    else:
                        self.AccProc[colName+"Num"] = 0
                        self.AccProc[colName+"Chips"] = 0

            for colName in hasCol:
                self.AccProc[colName+"Chips"] = math.floor(self.AccProc[colName+"Chips"])

        img = PilImg.fromarray(cv2.cvtColor(AProimg,cv2.COLOR_BGR2RGB))
        img = img.resize((int(img.size[0]*0.65),int(img.size[1]*0.65)))
        self.imgtk = ImageTk.PhotoImage(image = img)
        saveImg(Proimg,"acc",timestp)

    def getTolerance(self):
        sticker = int(self.tolerance[self.chip]['Sticker'])/self.ChipArea
        black = int(self.tolerance[self.chip]['Tape'])/self.ChipArea
        return sticker, black

    def update(self):
        sticker,black = self.getTolerance()
        for accApp in self.AccVar:
            self.AccVar[accApp].config(text=self.AccProc[accApp])
            if accApp[-5:] == "Chips":
                if accApp[:5] == "Black":
                    passfail = "green" if int(self.setAcc[accApp].get()) - black < int(self.AccProc[accApp]) < int(self.setAcc[accApp].get()) + black else "red"
                else:
                    passfail = "green" if int(self.setAcc[accApp].get()) - sticker < int(self.AccProc[accApp]) < int(self.setAcc[accApp].get()) + sticker else "red"
            else:
                passfail = "green" if int(self.setAcc[accApp].get()) == int(self.AccProc[accApp]) else "red"

            self.Canva[accApp].itemconfig("circle",fill=passfail)
