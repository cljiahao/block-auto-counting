import cv2
from Debug import *

with open('settings.json') as f:
	setData = json.load(f)
	TexCol = setData['Highlight']

#									For Putting Text on image
#########################################################################################################
def TextAdding(Finalimg,length,cnt,pieces,Textadd):
	if Textadd:	
		approx = cv2.approxPolyDP(cnt, 0.0001*cv2.arcLength(cnt, True), True)
		n = approx.ravel()                                                               # Used to flatted the array containing the co-ordinates of the vertices.
		
		# Numbered Found stickers
		x = n[-2] + 5
		y = n[-1] - 5

		if Finalimg.shape[0] < n[-2]*1.05:
			x = int(n[-2]*0.95)
		elif Finalimg.shape[1] < n[-1]*1.05:
			y = int(n[-1]*0.95)
		elif n[-2] <= Finalimg.shape[0]*0.05:
			x = int(Finalimg.shape[0]*0.05)
		elif n[-1] <= Finalimg.shape[1]*0.05:
			y = int(Finalimg.shape[1]*0.05)

		cv2.putText(Finalimg,f"{length:.0f}", (x, y),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 1)
		# cv2.putText(Finalimg,f"{pieces:.0f}", (n[-4]+5, n[-3]+30),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 1)
		cv2.drawContours(Finalimg,[approx],0,(255,255,255),1)
	return Finalimg

def oddTextAdd(Finalimg,cnt,M,a,type):
	
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])

	approx = cv2.approxPolyDP(cnt, 0.0001*cv2.arcLength(cnt, True), True)
	n = approx.ravel()                                                               # Used to flatted the array containing the co-ordinates of the vertices.

	for j in n:
		if type in TexCol.keys():
			cv2.putText(Finalimg,str(a),(cX,cY),cv2.FONT_HERSHEY_COMPLEX, 1, TexCol[type], 1)
			cv2.drawContours(Finalimg,[approx],0,(255,255,255),1)

	return Finalimg