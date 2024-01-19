import cv2
import math
import json
import numpy as np

from Debug import *

def Cali(image):

    """
    Mask image to retrieve far left Black pin contour
    Parameters
    ----------
    image : 3-D Image MAT
        Src input image
    """
    
    with open('settings.json') as f:
        setData = json.load(f)
        misc = setData['Misc']
        pindia = misc['Pin Size']
        colour = setData['colours']
        black = colour['Black']

    Area = (int(pindia)/2)**2*math.pi    
    img = image.copy()

    #######################################################################################################
    # IDEA 1: Mask Image based on Colour (HSV)
    
    # blur = cv2.GaussianBlur(img, (5, 5), 0)
    # hsvimg = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV_FULL)
    # Black_LL = np.array([int(x) for x in black['LL'].split(",")], dtype=np.uint8)
    # Black_UL = np.array([int(y) for y in black['UL'].split(",")], dtype=np.uint8)
    # black = cv2.inRange(hsvimg,Black_LL,Black_UL)  

    # cnts, _ = cv2.findContours(black.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # # Store found contours in dict and sort them to retrieve most left area
    # preSort = {}
    # for c in cnts:
    #     cntArea = cv2.contourArea(c)
    #     x,y,w,h = cv2.boundingRect(c)
    #     if cntArea > 300:
    #         if 50 < x & x < 200:
    #             preSort[x] = cntArea
                
    # pixArea = sorted(preSort.items())[0][1]

    #######################################################################################################
    # IDEA 2: Hough Circle to find circle and check if its black
    img = img[800:950,50:250]
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blank = np.zeros(img.shape[:2], np.uint8)

    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,2,20,param1=100,param2=30,minRadius=11,maxRadius=15)

    print(circles)

    for c in circles[0]:
        cv2.circle(blank,(int(c[0]),int(c[1])),int(c[2]),(255,255,255),-1)

    circleMask = cv2.bitwise_and(img,img,mask=blank)

    cnts, _ = cv2.findContours(blank, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    blur = cv2.GaussianBlur(circleMask, (5, 5), 0)
    hsvimg = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV_FULL)
    Black_LL = np.array([int(x) for x in black['LL'].split(",")], dtype=np.uint8)
    Black_UL = np.array([int(y) for y in black['UL'].split(",")], dtype=np.uint8)
    black = cv2.inRange(hsvimg,Black_LL,Black_UL)  

    for c in cnts:
        cntArea = cv2.contourArea(c)
        print(cntArea, np.sum(black))
        if cntArea > 300 and np.sum(black)>40000:
            pixArea = cntArea

    #######################################################################################################

    avgPixLen = (Area/pixArea)*0.9
    print(f'Calibration Pin: {avgPixLen:.4f} mm/pixel')

    return avgPixLen
