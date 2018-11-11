import cv2
import numpy as np

img = cv2.imread('example.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


ret,thresh = cv2.threshold(gray,107,255,0)

thresh = cv2.erode(thresh, np.ones((2,2), np.uint8), iterations=1)
thresh = cv2.dilate(thresh, np.ones((2,2), np.uint8), iterations=1)
#Morphological closing (fill small holes in the foreground)
thresh = cv2.dilate(thresh, np.ones((2,2), np.uint8), iterations=1)
thresh = cv2.erode(thresh, np.ones((2,2), np.uint8), iterations=1)

im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

if len(contours) != 0:

	c = sorted(contours, key = cv2.contourArea)[-3]
	x,y,w,h = cv2.boundingRect(c) # Determina el borde
	mask = np.zeros(img.shape, dtype = "uint8") #Aplica la máscara
	cv2.rectangle(mask, (x,y),(x+w,y+h), (255, 255, 255), -1)
	m_img = cv2.bitwise_and(img, mask)
# show the images
cv2.imshow("Result", m_img)

cv2.waitKey(0)