import cv2
import numpy as np
import os
import HandTrackingModule as htm

brushTh = 15
eraserTh = 100

folderPath = "images"
myList = os.listdir(folderPath)
#print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
#print(len(overlayList))
header = overlayList[3]

drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

detector = htm.handDetector()
xp, yp = 0, 0

while True:
    # 1-Import images
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2-Find hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        # Tip of the index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # 3-Check which fingers are up
        fingers = detector.fingersUP()
        # 4-If selection mode -Two Fingers UP-
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            #print("Selection MODE")
            # Check Clicking
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlayList[4]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5-If Drawing Mode -One Finger is UP-
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            #print("Drawing MODE")
            #start from where the hand is not the start(0,0)
            if xp == 0 and yp == 0:
                xp, yp= x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserTh)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserTh)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushTh)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushTh)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    #setting the header image
    img[0:125, 0:1280] = header
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("IMAGE", img)
    #cv2.imshow("IMAGE Canvas", imgCanvas)
    #cv2.imshow("IMAGE inv", imgInv)
    k = cv2.waitKey(33)
    if k == 27:  # Esc key to stop
        break

