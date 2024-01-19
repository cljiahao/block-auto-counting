import os
import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

i = 1
path = r"C:\Users\MES21106\Desktop\test"

while 1:
    dirpath = os.path.join(path,f"acc{i}.png")
    _,img = cap.read()

    cv2.imshow("img",img)
    cv2.imwrite(dirpath,img)
    cv2.waitKey(0)
    i+=1