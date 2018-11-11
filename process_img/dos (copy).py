#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
from scipy.cluster.vq import vq, kmeans
from matplotlib import pyplot as plt
import numpy as np
import time as t

cv_image = cv2.imread('/home/jose/Desktop/model_final.jpg',1)
cv_copy  = cv_image.copy()
#cv2.imshow('image',cv_image)
height, width , depth  = cv_image.shape
hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

thresholded = 0
obj_color = 0
if obj_color == 0: 

	#hsv
    low  = [0,50,100]
    up = [50,250,150]

    lower = np.array(low, np.uint8)
    upper = np.array(up, np.uint8)


    hue, sat, val = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]
    

    plt.figure(figsize=(10,8))
    plt.subplot(311)                             #plot in the first cell
    plt.subplots_adjust(hspace=.5)
    plt.title("Indicador H - Tonalidad")
    plt.hist(np.ndarray.flatten(hue), bins=180)
    plt.subplot(312)                             #plot in the second cell
    plt.title("Indicador S - Saturacion")
    plt.hist(np.ndarray.flatten(sat), bins=128)
    plt.subplot(313)                             #plot in the third cell
    plt.title("Indicador V - Valor Luminosidad")
    plt.hist(np.ndarray.flatten(val), bins=128)
    plt.show()

    thresholded = cv2.inRange(hsv, lower, upper)
    #Morphological opening (remove small objects from the foreground)
    thresholded = cv2.erode(thresholded, np.ones((2,2), np.uint8), iterations=1)
    thresholded = cv2.dilate(thresholded, np.ones((2,2), np.uint8), iterations=1)
    #Morphological closing (fill small holes in the foreground)
    thresholded = cv2.dilate(thresholded, np.ones((2,2), np.uint8), iterations=1)
    thresholded = cv2.erode(thresholded, np.ones((2,2), np.uint8), iterations=1)

    ret,thresh = cv2.threshold(thresholded,127,255,0)
    _, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    #contours= cv2.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #c = max(contours, key = cv2.contourArea)
    #cv2.drawContours(thresh,[c],0,(0, 255, 0),3)
    #bc = biggestContourI(contours)
    cv2.drawContours(cv_copy, contours, -1, (0,255,0),3)
    cv2.imshow('draw contours',cv_copy)
    print contours
    numobj = len(contours) # number of objects found in current frame
    print(numobj)
    if numobj > 0:
        print("here")
        moms = cv2.moments(contours[0])
        if moms['m00']>40:
            cx = int(moms['m10']/moms['m00'])
            cy = int(moms['m01']/moms['m00'])

            xb = -(cy - (height/2))*.0025*.428 + .578  
            yb = -(cx - (width/2))*.0025*.428 + .40  +0.06

            print("xb: ",xb)
            print("yb: ",yb)

        #print "Found blue ", numobj,  "object(s)" 
        obj_found = True
else:
    print "Couldn't find any green or blue objects."

#cv2.imshow("O", hsv)
cv2.imshow("Thresholded", thresholded)
cv2.waitKey(0)
