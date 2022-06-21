import cv2
import mediapipe as mp
import time


class FaceDetector():
    def __init__(self, minDetectionCon=0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findFaces(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                h, w, c = img.shape
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), \
                       int(bboxC.width * w), int(bboxC.height * h)
                # print(bbox)
                bboxs.append([id, bbox, detection.score])
                if draw:
                    img = self.fancyDraw(img, bbox)
                    cv2.putText(img, f'{int(detection.score[0]*100)}%', (bbox[0], bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        return img, bboxs

    def fancyDraw(self, img, bbox, l=30, t=5):
        x, y, w, h = bbox
        x1, y1 = x+w, y+h
        cv2.rectangle(img, bbox, (255, 0, 255), 1)
        # Top Left
        cv2.line(img, (x, y), (x+l, y), (0, 0, 255), t)
        cv2.line(img, (x, y), (x, y+l), (0, 0, 255), t)
        # Top Right
        cv2.line(img, (x1, y), (x1 - l, y), (0, 0, 255), t)
        cv2.line(img, (x1, y), (x1, y + l), (0, 0, 255), t)
        # Bottom Left
        cv2.line(img, (x, y1), (x + l, y1), (0, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1 - l), (0, 0, 255), t)
        # Bottom Right
        cv2.line(img, (x1, y1), (x1 - l, y1), (0, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (0, 0, 255), t)
        return img


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceDetector()
    while True:
        succ, img = cap.read()
        img, bboxs = detector.findFaces(img)
        print(bboxs)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()