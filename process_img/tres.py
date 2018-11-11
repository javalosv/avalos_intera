#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image
from scipy.cluster.vq import vq, kmeans
from matplotlib import pyplot as plt
import numpy as np
import time as t
from cv_bridge import CvBridge, CvBridgeError

#cv_image = cv2.imread('/home/jose/Desktop/model.png',1)
#cv_copy  = cv_image.copy()
def callback(img_data):
    #Capturing image of camera
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(img_data, "bgr8")
    cv_copy  = cv_image.copy()  
    cv2.imshow("Original", cv_copy)
    #cv2.imshow('image',cv_image)
    height, width , depth  = cv_image.shape
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    thresholded = 0
    obj_color = 0
    if obj_color == 0: 
        thresholded = cv2.erode(gray, np.ones((3,3), np.uint8), iterations=1)
        thresholded = cv2.dilate(thresholded, np.ones((2,2), np.uint8), iterations=1)

        thresholded = cv2.dilate(thresholded, np.ones((3,3), np.uint8), iterations=1)
        thresholded = cv2.erode(thresholded, np.ones((2,2), np.uint8), iterations=1)

        ret, thresh = cv2.threshold(thresholded, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #_, contours, hierarchy = cv2.findContours(hsv,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
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


def main():
    #Initiate left hand camera object detection node
    rospy.init_node('left_camera')
    #Create names for OpenCV images and orient them appropriately
    cv2.namedWindow("Original", 1)
    #cv2.namedWindow("Thresholded", 2)
    rospy.Subscriber("/io/internal_camera/right_hand_camera/image_raw", Image, callback)
    rospy.spin()


if __name__ == '__main__':
     main()
