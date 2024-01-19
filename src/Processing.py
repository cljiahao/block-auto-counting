import cv2
import math
import time
import numpy as np
import pandas as pd

from Debug import *
from Colours import *
from TextAdding import *
from OddSticker import *
from Calibration import *

# Fixed Parameters
##########################################################################################################################
def ProPara(chip):

	Col_Stick = []
	with open('settings.json') as f:
		setData = json.load(f)
		misc = setData['Misc']
		Texadd = misc['Trouble']
		ChipArea = float(setData['Chip Size'][chip]['L'])*float(setData['Chip Size'][chip]['W'])
		colours = setData['colours']

	for col in colours.keys():
		if col == "Black":
			Black_LL = np.array([int(x) for x in colours[col]['LL'].split(",")], dtype=np.uint8)
			Black_UL = np.array([int(y) for y in colours[col]['UL'].split(",")], dtype=np.uint8)
			Black_Stick = {"LL" : Black_LL, "UL" : Black_UL}
		else:
			Col_LL = np.array([int(x) for x in colours[col]['LL'].split(",")], dtype=np.uint8)
			Col_UL = np.array([int(y) for y in colours[col]['UL'].split(",")], dtype=np.uint8)
			Col_Stick.append({"LL" : Col_LL, "UL" : Col_UL})

	return Texadd, ChipArea, Col_Stick, Black_Stick

# Capture and Process to find Block perimeter
##########################################################################################################################

def ProcessCapture(img):

	blank = np.zeros(img.shape[:2], np.uint8)
	kernel = np.ones((19,19), np.uint8)
	ker = np.ones((51,51),np.uint8)

	lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
	l_channel, a, b = cv2.split(lab)

	clahe = cv2.createCLAHE(clipLimit=2.0)
	image = clahe.apply(l_channel)

	blur = cv2.medianBlur(image,9)
	thresh = cv2.bitwise_not(cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,3))
	morph = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel)
	cnt, hier = cv2.findContours(morph,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cn = sorted(cnt, key=lambda x: cv2.contourArea(x))[-1]
	mask = cv2.drawContours(blank.copy(),[cn],-1,(255,255,255),-1)
	mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	c, h = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	c = sorted(c, key=lambda x: cv2.contourArea(x))[-1]
	cv2.drawContours(blank,[c],0,(255,255,255),-1)
	blank = cv2.morphologyEx(blank,cv2.MORPH_OPEN,ker)
	cropImg = cv2.bitwise_and(img,img,mask=blank)

	dst = cv2.cornerHarris(blank,10,3,0.04)
	ret, dst = cv2.threshold(dst,0.2*dst.max(),255,0)
	dst = np.uint8(dst)
	ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

	df = pd.DataFrame(stats,columns=list(range(len(stats[0]))))
	print(df)
	index = df[(df[4]<100)].index
	cent = np.array([centroids[i].round(0).astype(int) for i in index])
	sumCen = cent.sum(axis=1)
	x1,x2,y1,y2 = cent[np.argmin(sumCen)][0],cent[np.argmax(sumCen)][0],cent[np.argmin(sumCen)][1],cent[np.argmax(sumCen)][1]
	Proimg = cropImg[y1-3:y2+3,x1-3:x2+3]

	return Proimg
#                                   Program Grayscale to find sticker perimeter
#########################################################################################################
def FindSticker(Proimg,Col_Stick,Black_Stick):

	black = cv2.inRange(cv2.cvtColor(Proimg,cv2.COLOR_BGR2HSV_FULL),Black_Stick["LL"],Black_Stick["UL"])
	mix = black

	Proimg = cv2.GaussianBlur(Proimg.copy(), (3, 3), 0)
	hsv = cv2.cvtColor(Proimg,cv2.COLOR_BGR2HSV_FULL)

	for i,j in enumerate(Col_Stick):
		thresh = cv2.inRange(hsv,j["LL"],j["UL"])
		thresh = cv2.erode(thresh,None)
		thresh = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,None)
		cn,hi = cv2.findContours(thresh.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		for a,c in enumerate(cn):
			aftcnt = np.zeros(thresh.shape[:2], np.uint8)
			if hi[0][a][2] == -1 and hi[0][a][3] == -1:
				# continue
				cv2.drawContours(aftcnt,[c],-1,color=(255,255,255),thickness=-1)
				aftcnt = cv2.dilate(aftcnt,None)
			# else:
			# 	cv2.drawContours(aftcnt,[c],-1,color=(255,255,255),thickness=-1)
			# 	aftcnt = cv2.dilate(aftcnt,None)
			mix = cv2.bitwise_or(mix,aftcnt)

	opening = cv2.morphologyEx(mix,cv2.MORPH_CLOSE,None)

	return opening

#                                   Math
####################################################a####################################################
def ChipPixelCount(Proimg,cnts,avgPixLen,ChipArea,Texadd,lotNum,Wscreen,Hscreen):

	Defects, oddDict = {},{}
	Fimg = Proimg.copy()
	Bimg = Proimg.copy()

	timestp = datetime.today().strftime("%d-%m-%y_%H%M%S")


	blur = cv2.GaussianBlur(Proimg.copy(), (5, 5), 0)
	hsvimg = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV_FULL)

	for cnt in cnts:
		if 100000<cv2.contourArea(cnt) or cv2.contourArea(cnt)<30:
			continue

		Moments = cv2.moments(cnt)
		cArea = cv2.contourArea(cnt)
		realsize = cArea*avgPixLen
		pieces = math.floor(realsize/ChipArea)
		length = math.sqrt(cArea*avgPixLen)

		preDefects,oddCol = StickerColor(hsvimg, cnt)

		for Def in preDefects:
			if preDefects[Def] > 0:
				if Def in Defects.keys():
					Defects[Def] += pieces
				else:
					Defects[Def] = pieces
				Fimg = TextAdding(Fimg,length,cnt,pieces,Texadd)
			else:
				if Def in Defects.keys():
					Defects[Def] += 0
				else:
					Defects[Def] = 0

		for Col,val in oddCol.items():
			if Col in TexCol.keys():
				if Col not in oddDict:
					oddDict[Col] = []
				if val > 0:
					oddDict[Col].append(pieces)
					Bimg = oddTextAdd(Bimg,cnt,Moments,len(oddDict[Col]),Col)
			if oddCol[Col] > 0:
				dataLog(lotNum,[timestp,avgPixLen,Col,cArea,realsize])

	if bool([a for a in oddDict.values() if a !=[]]):
		odd_Win = OddStick_Window(oddDict,Bimg,Wscreen,Hscreen)
		odd_def = odd_Win.selected
		odd_Win.root.destroy()
		for key,value in odd_def.items():
			for k in value.keys():
				if k in Defects.keys():
					Defects[k] += odd_def[key][k]
				else:
					Defects[k] = odd_def[key][k]

	return Fimg,Defects

#                                   Main Program for processing Image
#########################################################################################################
def mainPro(img,chip):
	Texadd, ChipArea, Col_Stick, Black_Stick = ProPara(chip)
	avgPixLen = Cali(img)
	Proimg = ProcessCapture(img)
	opening = FindSticker(Proimg,Col_Stick,Black_Stick)

	cnts, hier = cv2.findContours(opening.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	return Proimg,cnts,avgPixLen,ChipArea,Texadd

#                                   For Main Process / Workflow Usage
#########################################################################################################
def Capture(img,chip,lotNum,Wscreen,Hscreen):

	start = time.time()
	Proimg,cnts,avgPixLen,ChipArea,Texadd = mainPro(img,chip)
	print("Process Image End: ",time.time()-start)
	start = time.time()
	Fimg,Defects = ChipPixelCount(Proimg,cnts,avgPixLen,ChipArea,Texadd,lotNum,Wscreen,Hscreen)
	print("Chip Count End: ",time.time()-start)

	return Fimg, Defects


