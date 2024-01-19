import json
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class showFinal():

    """
    Toplevel for showFinal Widget and selenium to showFinal PRASS
    Parameters
    ----------
    df : DataFrame
        DataFrame from previous Class to show final output.
    lotnum : str
        Lot Number associated with the file sent.
    Wscreen : str
        Providing Screen Size (Width) to Class.
    Hscreen : str
        Providing Screen Size (Height) to Class.
    """

    def __init__(self,df,lotnum,Wscreen,Hscreen):

        with open('settings.json') as f:
            setData = json.load(f)
            config = setData['Config']
            self.url = config['PRASS']
            self.font = setData['font']['normal']

        self.df = df
        self.lotnum = lotnum
        self.root = Toplevel()
        self.root.title("Final Window")
        self.Wscreen, self.Hscreen = Wscreen, Hscreen
        self.root.geometry(f"{int(Wscreen*1/5)}x{int(Hscreen*0.95)}+{int(Wscreen*4/5*0.99)}+0")
        self.frame = Frame(self.root)
        self.frame.rowconfigure(2,weight=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.getPrass()
        self.totalDef()
        self.root.grab_set()
        self.root.mainloop()

    def getPrass(self):

        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_experimental_option('detach',True)

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=chrome_options)
        self.driver.get(self.url)
        self.driver.set_window_position(x=0,y=0)
        self.driver.set_window_size(int(self.Wscreen*4/5),self.Hscreen)
        try:
            self.driver.switch_to.frame(self.driver.find_element(By .NAME, 'up'))
            self.driver.find_element(By .NAME, 'Lotno').send_keys(self.lotnum)
            self.driver.find_element(By .NAME, 'Search').click()
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(self.driver.find_element(By .NAME, 'down'))
            self.driver.find_element(By .XPATH,'/html/body/table[2]/tbody/tr[6]/td[3]/font').location_once_scrolled_into_view
        except:
            pass

    def totalDef(self):
        # Labelframe for Lot Number Data
        ###########################################################################
        lotNumCont = LabelFrame(self.frame, bd=5, relief=FLAT)
        lotNumCont.grid(row=0, column=0, padx=3, pady=1,sticky=W)
        
        lotNumTxt = Label(lotNumCont, text="Lot Number: ", font=("Courier",13))
        lotNumTxt.grid(row=0, column=0, padx=3, pady=1, sticky=W)

        lotNum = Label(lotNumCont, text=self.lotnum, font=("Courier",13))
        lotNum.grid(row=0, column=1, padx=3, pady=1)

        # # Labelframe for Defects Data
        # ###########################################################################

        self.dataCont = LabelFrame(self.frame, bd=5, relief=FLAT)
        self.dataCont.grid(row=1, column=0, pady=1, padx=10)

        for i,j in enumerate(self.df.index):
            Label(self.dataCont, text=j,font=self.font).grid(row=i+1,column=0, pady=1, padx=15, sticky=W)
            Label(self.dataCont, text=self.df.loc[j][0],font=self.font).grid(row=i+1,column=1, pady=1, padx=15, sticky=W)

        self.butFrame = LabelFrame(self.frame,bd=5, relief=FLAT)
        self.butFrame.grid(row=3, column=0, pady=1, padx=10)
        
        Button(self.butFrame,text="Okay",pady=10,width=10,command=lambda: self.close()).grid(row=0,column=0,columnspan=2,sticky=S)

    def close(self):
        self.res = True
        self.root.quit()
        self.root.destroy()
        self.driver.quit()