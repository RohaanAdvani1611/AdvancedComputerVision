import cv2
import math
import HandTrackingModule as htm

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]


def convert_sign(arr, ori, length, length2, sc1, sc2, sc3, sc4):
    alp = ''
    if sc3 == 'X':
        alp = 'X'
    else:
        if ori == 'Vertical':
            if arr == [0, 0, 0, 0, 0]:
                if sc2 == 'A':
                    alp = 'A'
                if sc2 == 'E':
                    alp = 'E'
                if sc2 == 'S':
                    alp = 'S'
                if sc2 == 'T':
                    alp = 'T'
            if arr == [0, 1, 1, 1, 1]:
                alp = 'B'
            if arr == [0, 1, 0, 0, 0]:
                alp = 'D'
            if arr == [0, 0, 1, 1, 1]:
                alp = 'F'
            if arr == [0, 0, 0, 0, 1]:
                alp = 'I'
            if arr == [1, 1, 0, 0, 0]:
                alp = 'L'
            if arr == [0, 1, 1, 1, 0]:
                alp = 'W'
            if arr == [1, 0, 0, 0, 1]:
                alp = 'Y'
            if arr == [0, 1, 1, 0, 0]:
                if sc1 == 'K':
                    alp = 'K'
                else:
                    if length < 20:
                        alp = 'R'
                    elif length > 20 and length < 30:
                        alp = 'U'
                    else:
                        alp = 'V'
        else:
            if arr == [0, 1, 0, 0, 0]:
                alp = 'G'
            if arr == [0, 1, 1, 0, 0]:
                alp = 'H'
            if arr == [1, 1, 1, 1, 1]:
                if length2 > 30:
                    alp = 'C'
                else:
                    alp = 'O'
            if arr == [0, 0, 0, 0, 0]:
                if sc4 == 'N':
                    alp = 'N'
                else:
                    alp = 'M'
    return alp


while True:
    succ, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        fingers1 = []
        fingers2 = []

        # Thumb X
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers1.append(1)
        else:
            fingers1.append(0)

        # Thumb Y
        if lmList[tipIds[0]][2] > lmList[tipIds[0] - 2][2]:
            fingers2.append(0)
        else:
            fingers2.append(1)

        # 4 Fingers Y
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers1.append(1)
            else:
                fingers1.append(0)

        # 4 Fingers X
        for id in range(1, 5):
            if lmList[tipIds[id]][1] < lmList[tipIds[id] - 1][1]:
                fingers2.append(1)
            else:
                fingers2.append(0)

        # Orientation
        count = 0
        ori = ''
        for id in range(2, 21):
            if lmList[0][1] > lmList[id][1]:
                count += 1
            if count == 19:
                ori = 'Horizontal'
            else:
                ori = 'Vertical'

        # Distance between index and middle
        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[12][1], lmList[12][2]
        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Distance between index and thumb
        x1, y1 = lmList[8][1], lmList[8][2]
        x3, y3 = lmList[4][1], lmList[4][2]
        length2 = math.hypot(x3 - x1, y3 - y1)
        # print(length2)

        # Special Cases:
        sc1 = ''
        sc2 = ''
        sc3 = ''
        sc4 = ''
        sc5 = ''
        if lmList[8][2] < lmList[5][2] and fingers1 == [0, 0, 0, 0, 0]:
            sc3 = 'X'
        if lmList[4][1] < lmList[8][1] and lmList[4][1] > lmList[12][1]:
            sc1 = 'K'
            sc2 = 'T'
        if lmList[4][1] > lmList[8][1]:
            sc2 = 'A'
        if lmList[4][1] < lmList[12][1] and lmList[4][1] > lmList[20][1]:
            sc2 = 'S'
        if lmList[4][1] < lmList[20][1]:
            sc2 = 'E'
        if lmList[10][2] < lmList[6][2] and ori == 'Horizontal':
            sc4 = 'N'
        if lmList[4][2] > lmList[0][2] and lmList[12][2] > lmList[0][2]:
            sc5 = 'P'
        if lmList[4][2] > lmList[0][2] and lmList[8][2] > lmList[0][2]:
            sc5 = 'Q'
        if sc5:
            alp = sc5
        else:
            if ori == 'Vertical':
                alp = convert_sign(fingers1, ori, length, length2, sc1, sc2, sc3, sc4)
            else:
                alp = convert_sign(fingers2, ori, length, length2, sc1, sc2, sc3, sc4)
        cv2.putText(img, alp, (40, 400), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 3)

        # print(fingers1)
        # print(fingers2)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
