import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

cv2.namedWindow("img",cv2.WINDOW_FREERATIO)

while True:
    _, img = cap.read()
    img = img[:,int(1920/6):int(1920/6*5)]
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV_FULL)
    img = cv2.inRange(hsv,(0,1,115),(255,40,145))

    cv2.imshow("img",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break