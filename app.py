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

        self.img = cv2.resize(self.img, (0, 0), None, 0.2, 0.2)
        self.size = self.img.shape[:2]

    def update(self, cursor, otherObjects):
        ox, oy = cursor[0] - self.size[1] // 2, cursor[1] - self.size[0] // 2
        h, w = self.size

        # Check if the new position is valid (no collision with other objects)
        valid_position = all(
            not (ox < obj.posOrigin[0] + obj.size[1] and
                 ox + w > obj.posOrigin[0] and
                 oy < obj.posOrigin[1] + obj.size[0] and
                 oy + h > obj.posOrigin[1])
            for obj in otherObjects if obj != self
        )

        if valid_position:
            self.posOrigin = (ox, oy)


path = "Images"
pathImg = os.path.join(path, '1.png')

listImg = []
n = 4

for x in range(n):
    listImg.append(DragImg(f'{pathImg}', [50 + x * 300, 100], imgType = 'png'))

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

        if length < 100:
            cursor = lmList[8]
            for imgObject in listImg:
                imgObject.update(cursor, listImg)

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