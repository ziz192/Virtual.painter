import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
####################################
wCAM, hCAM = 640, 480
####################################

cap = cv2.VideoCapture(0)
cap.set(3, wCAM)
cap.set(4, hCAM)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-5.0, None)

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
#volBar = 400

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #$print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1,y1), 10, (255,0,0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (155, 0, 0), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (0, 255, 0), 2)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        print(length)

        # Hand Range 50 ~ 300
        # Volume Range  -65 ~ 0

        vol = np.interp(length, [40, 200], [minVol, maxVol])
        volBar = np.interp(length, [40, 200], [400, 150])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 40:
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

    # cv2.rectangle(img, (50,150), (85, 400), (255,0,0), 2)
    # cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), 3, cv2.FILLED)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (30, 50), cv2.FONT_ITALIC, 1, (255,0,0), 2)

    cv2.imshow("Img", img)
    cv2.waitKey(1)