import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import os

cap = cv2.VideoCapture(0)
width, height = 1280, 720
cap.set(3, 1600)
cap.set(4, 1200)
hs, ws = int(height * 0.2), int(width * 0.17)  # width and height of small image

detector = HandDetector(detectionCon=0.8)

class DragImg():
    def __init__(self, path, posOrigin, imgType):

        self.posOrigin = posOrigin
        self.imgType = imgType
        self.path = path

        if self.imgType == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        self.img = cv2.resize(self.img, (0,0),None,0.4,0.4)   
        self.size = self.img.shape[:2]

    def update(self, cursor):
        ox, oy = self.posOrigin
        h, w = self.size

        # Check if in region
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2
            # Update the background image with the new position
            self.background = cvzone.overlayPNG(background, self.img, self.posOrigin)

path = "Images"
pathImg = os.path.join(path, '1.png')

listImg = []
n = 4

for x in range(n):
    if 'png' in pathImg:
        imgType = 'png'
    else:
        imgType = 'jpg'
    listImg.append(DragImg(f'{pathImg}', [50 + x * 300, 50], imgType))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    background = cv2.imread('Christmas-tree.png')
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        # Check if clicked
        length, info, background = detector.findDistance((lmList[8][0], lmList[8][1]), 
                                       (lmList[12][0], lmList[12][1]), background)

        if length < 60:
            cursor = lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor)

    try:

        for imgObject in listImg:

            # Draw for JPG image
            h, w = imgObject.size
            ox, oy = imgObject.posOrigin
            if imgObject.imgType == "png":
                # Draw for PNG Images
                background = cvzone.overlayPNG(background, imgObject.img, [ox, oy])
            else:
                background[oy:oy + h, ox:ox + w] = imgObject.img

    except:
        pass

    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = background.shape
    background[0:hs, w - ws: w] = imgSmall

    cv2.imshow("Christmas Tree", background)
    #cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == 27:  # Check for the "Escape" key (ASCII code 27)
        break