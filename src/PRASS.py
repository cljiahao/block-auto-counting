import os
import json
import requests
import pandas as pd
from datetime import datetime
from tkinter import messagebox

from showFinal import *

class PRASS():

    """
    Open Lot File, extract and clean data, summarise and send to PRASS.
    Parameters
    ----------
    lotnum : str
        Lot Number.
    mcno : str
        Machine Number.
    payroll : str
        Payroll Number.
    inQty : strs
        Input Quantity.
    Wscreen : str
        Providing Screen Size (Width) to Class.
    Hscreen : str
        Providing Screen Size (Height) to Class.
    """

    def __init__(self,lotnum,mcno,payroll,inQty,Wscreen,Hscreen,filepath):

        with open('settings.json') as f:
            setData = json.load(f)
            config = setData['Config']
            self.url = config['fileServer']
            self.defCode = setData['staticName']['defCode']

        self.lotNumb = lotnum
        self.mcno = mcno
        self.payroll = payroll
        self.inQty = inQty
        self.Wscreen,self.Hscreen = Wscreen,Hscreen
        self.filepath = filepath
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"prass",datetime.today().strftime("%b%y"))
        self.Sum_Data()

    # Sending txt file to PRASS
    def send_PRASS(self, pData):
        self.res = messagebox.askyesno(title="Send Data To PRASS", message="Confirm Send Data?")
        if self.res:
            try:
                with open(os.path.join(self.path,f'{self.lotNumb}.txt'), 'w') as f:
                    f.write(pData)

                    # To send via FTP
                    """
                    with FTP("163.50.33.28","s8pc","prasspc") as ftp:
                    ftp.cwd('/fa/thermal_release/')
                    file = open(os.path.join(self.path,f'{self.lotNumb}.txt'),'rb')
                    ftp.storbinary(f'STOR {self.lotNumb}.txt',file)
                    file.close()
                    ftp.quit()
                    """

                # To Send via HTTP
                files = {'file': open(os.path.join(self.path,f'{self.lotNumb}.txt'), 'rb')}
                resp = requests.post(self.url, files=files)
                print(f"filesize: {int(resp.content)}")
                # Request OK, bring up website and final quantity for final cross check
                # if resp.ok:
                if int(resp.content) == os.stat(os.path.join(self.path,f'{self.lotNumb}.txt')).st_size:
                    self.res = showFinal(self.newdf,self.lotNumb,self.Wscreen,self.Hscreen).res
            except:
                messagebox.showwarning(title="Error while sending",message="File not sent to PRASS. Contact ME.") 
        
    # Create file spec format for sending to PRASS
    def create_PRASS(self, df):
        self.newdf = df.drop(columns=df.columns[0:-1])
        self.newdf.loc["Output"] = int(self.inQty) - int(self.newdf.loc['Total Defects','Total'])

        date = datetime.now().strftime("%Y/%m/%d")
        time = datetime.now().strftime("%H:%M:%S")

        df = df.loc[(df!=0).any(axis=1)]

        # Consolidate retrieved defects
        prassDef = ""
        for i, dataQty in enumerate(df["Total"]):
            if i < len(df["Total"]) - 1:
                prassDef += f"{self.defCode[df.index[i]]}|{dataQty}|" 

        # Range predetermined (Can be changed to increase)
        for j in range(10-(len(df["Total"])-1)):
            if j != range(10-(len(df["Total"])-1))[-1]:
                prassDef += "||" 
            else:
                prassDef += "|"

        # File Spec to follow
        pData = f"{self.lotNumb}|{self.mcno}|{self.payroll}|{date}|{time}|{self.inQty}|{self.newdf.loc['Output','Total']}|{prassDef}"

        self.send_PRASS(pData)
    # Data Cleanup and Summation of Data
    def Sum_Data(self):
        self.prasspath = os.path.join(os.path.dirname(os.path.dirname(__file__)),"prass",os.path.split(os.path.dirname(self.filepath))[-1])
        if not os.path.exists(self.prasspath): os.makedirs(self.prasspath)

        df = pd.read_excel(self.filepath, header=None)

        df = df[:].reset_index(drop=True).set_index(df.columns[0])

        df['Total'] = df.sum(axis = 1, skipna = True)
        df.loc['Total Defects'] = df.sum(axis = 0, skipna = True) 

        df = df.iloc[:,-1:]  

        self.create_PRASS(df)