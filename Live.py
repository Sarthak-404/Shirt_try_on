import os
import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
detector = PoseDetector()
listShirts = os.listdir(r'C:\Users\sarth\OneDrive\Documents\OpenCV\Resources\Shirts')
fixedRatio = 262 / 190
shirtRatioHeightWidth = 581 / 440
imageNumber = 0
imgButtonRight = cv2.imread(r'C:\Users\sarth\OneDrive\Documents\OpenCV\Resources\button.png', cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

def rescaleFrame(frame, scale = 2):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize( frame, dimensions, interpolation= cv2.INTER_AREA )

while True:
    isTrue, img = cap.read()
    img = rescaleFrame(img)
    img = detector.findPose(img)
    
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        lm11 = lmList[11][0:2]
        lm12 = lmList[12][0:2]
        imgShirt = cv2.imread(os.path.join(r'C:\Users\sarth\OneDrive\Documents\OpenCV\Resources\Shirts',listShirts[imageNumber]),cv2.IMREAD_UNCHANGED)
        imgShirt = cv2.resize(imgShirt,(0,0),None,0.5,0.5)
        widthofShirt = int((lm11[0] - lm12[0]) * fixedRatio)
        imgShirt = cv2.resize(imgShirt,(widthofShirt, int(widthofShirt * shirtRatioHeightWidth)))
        currentScale = (lm11[0] - lm12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)
        try:
            img = cvzone.overlayPNG(img,imgShirt,(lm12[0] - offset[0],lm12[1] - offset[1]))
        except:
            pass

    img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
    img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

    if lmList[16][0] < 300:
        counterRight += 1
        cv2.ellipse(img,(139,360),(66,66),0,0,counterRight*selectionSpeed,(0,255,0),20)
        if counterRight * selectionSpeed > 360:
            counterRight = 0
            if imageNumber < len(listShirts) - 1:
                imageNumber += 1 
    elif lmList[15][0] > 900:
        counterLeft += 1
        cv2.ellipse(img,(1138,360),(66,66),0,0,counterLeft*selectionSpeed,(0,255,0),20)
        if counterLeft * selectionSpeed > 360:
            counterLeft = 0
            if imageNumber > 0:
                imageNumber -= 1

    else:
        counterLeft = 0
        counterRight = 0

    cv2.imshow("Try",img)
    if cv2.waitKey(20) & 0xFF==ord('d'):
        break

cap.release()
cv2.destroyAllWindows()