import cv2
import numpy as np
import HandVideoControl as htm

#######################
brushThickness = 25
eraserThickness = 100
########################

headerList = [] 
imagem = cv2.imread("gt.png")

drawColor = (255, 0, 255)

cap = cv2.VideoCapture(1)
width = int(cap.get(4))
height = int(cap.get(3))
cap.set(3, height)
cap.set(4, width)

detector = htm.handDetector(detectionCon=0.7,maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((width, height, 3), np.uint8)

while True:

    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        # print(lmList)

        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # 4. If Eraser Mode - Two finger are up
        if fingers[1] and fingers[2] and fingers[3]== 0 and fingers[4] == 0 and fingers[0] == 0:
            
            drawColor = (255,0,255)
            
                
        if fingers[1] and fingers[2] == 0 and fingers[3]== 0 and fingers[4] == 0 and fingers[0] == 0:
            drawColor = (0, 0, 0)
        # 5. If Drawing Mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            
            xp, yp = 0, 0
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            #print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            
            if drawColor == (0, 0, 0):
                cv2.line(imagem, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            
            else:
                cv2.line(imagem, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                 
                 
            xp, yp = x1, y1


        # # Clear Canvas when all fingers are up
           # if fingers[0] == 0 and fingers[1] == 1 and fingers[2]==1 and fingers[3]==0 and fingers[4] == 0:
            #    img = np.zeros((480, 640, 3), np.uint8)

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    imagem = cv2.bitwise_and(imagem,imgInv)
    imagem = cv2.bitwise_or(imagem,imgCanvas)


    # Setting the header image
    #imgCanvas[0:480, 0:680] = header
    #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image", imagem)
    cv2.imshow("Cam",img)
    #cv2.imshow("Canvas", imgCanvas)
    #cv2.imshow("Inv", imgInv)
    cv2.waitKey(1)