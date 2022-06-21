import cv2
import HandTrackingModule as htm
import numpy as np

brushThickness = 15
eraserThickness = 50

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = htm.handDetector(detectionCon=0.75)
drawColor = (255, 0, 0)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    cv2.rectangle(img, (0, 0), (1280, 125), (0, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (10, 10), (320, 115), (255, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (330, 10), (640, 115), (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (650, 10), (950, 115), (0, 0, 255), cv2.FILLED)
    cv2.rectangle(img, (960, 10), (1270, 115), (255, 255, 255), cv2.FILLED)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            cv2.rectangle(img, (x1, y1-25), (x2, y2+25), drawColor, cv2.FILLED)
            if y1 < 125:
                if 10 < x1 < 320:
                    cv2.rectangle(img, (10, 10), (320, 115), (255, 0, 255), 3)
                    drawColor = (255, 0, 0)
                if 330 < x1 < 640:
                    cv2.rectangle(img, (330, 10), (640, 115), (255, 0, 255), 3)
                    drawColor = (0, 255, 0)
                if 650 < x1 < 950:
                    cv2.rectangle(img, (650, 10), (950, 115), (255, 0, 255), 3)
                    drawColor = (0, 0, 255)
                if 960 < x1 < 1270:
                    cv2.rectangle(img, (960, 10), (1270, 115), (255, 0, 255), 3)
                    drawColor = (0, 0, 0)
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)
