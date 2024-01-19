from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from Utils.readSettings import readSettings

class showFinal(readSettings):
    def __init__(self,root,df,Wscreen,Hscreen,lotNum="22X0282300"):
        super().__init__()
        self.root = Toplevel(root)
        # self.initialize()
        self.win_config(int(Wscreen),int(Hscreen))
        self.getPrass(lotNum,int(Wscreen),int(Hscreen))
        self.widgets(df,lotNum)
        self.root.grab_set()
        self.root.mainloop()

    # def initialize(self):

    def win_config(self,Wscreen,Hscreen):
        self.root.title("Final Window")
        self.Wscreen, self.Hscreen = Wscreen, Hscreen
        self.root.geometry(f"{int(Wscreen*1/5)}x{int(Hscreen*0.95)}+{int(Wscreen*4/5*0.99)}+0")
        self.frame = Frame(self.root)
        self.frame.rowconfigure(2,weight=1)
        self.frame.pack(fill=BOTH, expand=True)

    def widgets(self,df,lotNum):

        # Labelframe for Lot Number Data
        ####################################################################################################
        lotNumCont = LabelFrame(self.frame, bd=5, relief=FLAT)
        lotNumCont.grid(row=0, column=0, padx=3, pady=1,sticky=W)
        
        lotNumTxt = Label(lotNumCont, text="Lot Number: ", font=("Courier",13))
        lotNumTxt.grid(row=0, column=0, padx=3, pady=1, sticky=W)

        lotNumb = Label(lotNumCont, text=lotNum, font=("Courier",13))
        lotNumb.grid(row=0, column=1, padx=3, pady=1)

        # Labelframe for Defects Data
        ####################################################################################################
        self.dataCont = LabelFrame(self.frame, bd=5, relief=FLAT)
        self.dataCont.grid(row=1, column=0, pady=1, padx=10)

        for i,j in enumerate(df.index):
            Label(self.dataCont, text=j,font=self.font['M']).grid(row=i+1,column=0, pady=1, padx=15, sticky=W)
            Label(self.dataCont, text=df.loc[j][0],font=self.font['M']).grid(row=i+1,column=1, pady=1, padx=15, sticky=W)

        self.butFrame = LabelFrame(self.frame,bd=5, relief=FLAT)
        self.butFrame.grid(row=3, column=0, pady=1, padx=10)
        
        Button(self.butFrame,text="Okay",pady=10,width=10,command=lambda: self.close()).grid(row=0,column=0,columnspan=2,sticky=S)

    def getPrass(self,lotNum,Wscreen,Hscreen):

        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_experimental_option('detach',True)

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=chrome_options)
        self.driver.get(self.address["PRASS"])
        self.driver.set_window_position(x=0,y=0)
        self.driver.set_window_size(int(Wscreen*4/5),Hscreen)

        self.driver.switch_to.frame(self.driver.find_element(By .NAME, 'up'))
        self.driver.find_element(By .NAME, 'Lotno').send_keys(lotNum)
        self.driver.find_element(By .NAME, 'Search').click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element(By .NAME, 'down'))
        self.driver.find_element(By .XPATH,'/html/body/table[2]/tbody/tr[6]/td[3]/font').location_once_scrolled_into_view

    def close(self):
        self.res = False
        self.root.destroy()
        self.root.quit()
        self.driver.quit()