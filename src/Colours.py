import cv2
import numpy as np

from Debug import *

# Retrieve Color Data from Setting excel file
#########################################################################################################

def colSettings():

    """
    Retrieve Colour Range Parameters from json file
    Parameters
    ----------
    """

    with open('settings.json') as f:
        setData = json.load(f)
        defCode = setData['staticName']['defCode']
        colours = setData['colours']
        fixDef = setData['fixedDef']

    colDict = {}

    for col in colours:
        Col_LL = np.array([int(x) for x in colours[col]['LL'].split(",")], dtype=np.uint8)
        Col_UL = np.array([int(y) for y in colours[col]['UL'].split(",")], dtype=np.uint8)
        colDict[col] = {"LL" : Col_LL, "UL" : Col_UL}

    return colDict, defCode, fixDef

# Sticker Colour Configs (RGB)  
#########################################################################################################
def StickerColor(hsv,cnt):

    """
    Look for existing colours based on masked image
    Parameters
    ----------
    hsv : 3-D Image MAT
        Src input image
    cnt : 
        Contours of found defects
    """

    # Colour checking
    blank = np.zeros(hsv.shape[:2], np.uint8)
    cv2.drawContours(blank,[cnt],0,(255,255,255),-1)
    Stick_Mask = cv2.bitwise_and(hsv,hsv,mask=blank)

    colDict, defCode, fixDef = colSettings()

    Defects, hasCol = {}, {}
    for defects in defCode:
        Defects[defects] = 0

    for col in colDict:
        mask = cv2.inRange(Stick_Mask,colDict[col]['LL'],colDict[col]['UL'])
        hasCol[col] = np.sum(mask)

        if col == "Black":
            if hasCol[col] < 10000:
                hasCol[col] = 0
                
    maxKey = max(hasCol,key=hasCol.get)
    maxVal = hasCol[maxKey]
    hasCol = hasCol.fromkeys(hasCol,0)
    hasCol[maxKey] = maxVal

    for i in fixDef:
        for j in hasCol:
            if i == j:
                Defects[fixDef[i]] += hasCol[j]
            else:
                Defects[fixDef[i]] += 0

    return Defects, hasCol