import os
import shutil
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

############### Parameters ###############

folders = {}

folders["data"]     =   [ 3 , "Months" ]
folders["imglog"]   =   [ 3 , "Weeks" ]
folders["log"]      =   [ 3 , "Months" ]
folders["prass"]    =   [ 3 , "Months" ]
folders["acclog"]   =   [ 3 , "Months" ]
folders["acc"]      =   [ 3 , "Months" ]

##########################################

def dateFormat(strDict):
    
    num, dateForm = strDict
    mths, wks, days = 0,0,0

    if dateForm.lower() == "months":
        mths = num
    elif dateForm.lower() == "weeks":
        wks = num
    elif dateForm.lower() == "days":
        days = num      

    return mths, wks, days


path = os.path.dirname(os.path.dirname(__file__)) #stored in misc folder

for i in folders.keys():
    mths, wks, days = dateFormat(folders[i])
    prevTime = dt.now() - relativedelta(months=mths,weeks=wks,days=days)
    prevData = prevTime.strftime("%b%y")
    prevPath = os.path.join(path,i,prevData)
    if folders[i][1].lower() == "months":
        if os.path.exists(prevPath): shutil.rmtree(prevPath)
    try:
        for j in os.listdir(prevPath):
            filePath = os.path.join(prevPath,j)
            # print(dt.fromtimestamp(os.path.getctime(filePath)) < prevTime)
            if dt.fromtimestamp(os.path.getctime(filePath)) < prevTime:
                os.remove(filePath)
    except:
        pass


