#!/usr/local/bin/python
import cv2
import numpy as np

cv2.namedWindow("original")
cv2.namedWindow("preview")
cv2.namedWindow("circles")
vc = cv2.VideoCapture(1)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.waitKey(1)
    rval, frame = vc.read()
    img = cv2.medianBlur(frame,5)
    cv2.imshow("original",img)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,107,255,0)

    #thresh = cv2.erode(thresh, np.ones((2,2), np.uint8), iterations=1)
    #thresh = cv2.dilate(thresh, np.ones((2,2), np.uint8), iterations=1)
    #Morphological closing (fill small holes in the foreground)
    #thresh = cv2.dilate(thresh, np.ones((2,2), np.uint8), iterations=1)
    #thresh = cv2.erode(thresh, np.ones((2,2), np.uint8), iterations=1)

    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:

        c = sorted(contours, key = cv2.contourArea)[-3]
        x,y,w,h = cv2.boundingRect(c) # Determina el borde
        mask = np.zeros(img.shape, dtype = "uint8") #Aplica la mascara
        cv2.rectangle(mask, (x,y),(x+w,y+h), (255, 255, 255), -1)
        m_img = cv2.bitwise_and(img, mask)
        # show the images
        cv2.imshow("preview", m_img)

        #cimg = cv2.cvtColor(m_img,cv2.COLOR_GRAY2BGR)
        circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,param1=120,param2=40,minRadius=10,maxRadius=30)

        if circles is None:
            cv2.imshow("circles", img)
            continue
        circles = np.uint16(np.around(circles))

        for i in circles[0,:]:
           print i
           cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),4) # draw the outer circle
           cv2.circle(img,(i[0],i[1]),2,(0,0,255),4) # draw the center of the circle

        cv2.imshow("circles", img)
    key = cv2.waitKey(20)

    if key == 27: # exit on ESC
        break