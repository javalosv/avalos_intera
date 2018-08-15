import numpy as np
import cv2
from scipy.cluster.vq import vq, kmeans
from matplotlib import pyplot as plt
import numpy as np
import time as t

cv_image = cv2.imread('/home/jose/Desktop/dos.jpeg',1)
#cv_image = cv2.resize(img, (600, 450)) 
#img0 = cv2.medianBlur(img,5)
#cv_image = cv2.cvtColor(img0,cv2.COLOR_GRAY2BGR)
height, width , depth  = cv_image.shape
#print height, width, depth 
#Converting image to HSV format
hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

thresholded = 0
obj_color = 0
if obj_color == 0: 
    low_h  = 10
    low_s  = 0
    low_v  = 100
    

    high_h = 30    
    high_s = 200
    high_v = 250

    hue, sat, val = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]
    thresholded = cv2.inRange(hsv, np.array([low_h, low_s, low_v]), np.array([high_h, high_s, high_v]))

    plt.figure(figsize=(10,8))
    plt.subplot(311)                             #plot in the first cell
    plt.subplots_adjust(hspace=.5)
    plt.title("Hue")
    plt.hist(np.ndarray.flatten(hue), bins=180)
    plt.subplot(312)                             #plot in the second cell
    plt.title("Saturation")
    plt.hist(np.ndarray.flatten(sat), bins=128)
    plt.subplot(313)                             #plot in the third cell
    plt.title("Luminosity Value")
    plt.hist(np.ndarray.flatten(val), bins=128)
    #plt.show()

    #Morphological opening (remove small objects from the foreground)
    thresholded = cv2.erode(thresholded, np.ones((2,2), np.uint8), iterations=1)
    thresholded = cv2.dilate(thresholded, np.ones((2,2), np.uint8), iterations=1)
    #Morphological closing (fill small holes in the foreground)
    thresholded = cv2.dilate(thresholded, np.ones((2,2), np.uint8), iterations=1)
    thresholded = cv2.erode(thresholded, np.ones((2,2), np.uint8), iterations=1)

    ret,thresh = cv2.threshold(thresholded,255,255,0)

    contours= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    cv2.drawContours(cv_image, contours[1], -1, (0,255,0), 3)
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

            print("xb: ",xb,"/n")
            print("yb: ",yb,"/n")

        #print "Found blue ", numobj,  "object(s)" 
        obj_found = True
else:
    print "Couldn't find any green or blue objects."

#cv2.imshow("O", hsv)
cv2.imshow("Thresholded", thresholded)
cv2.waitKey(0)