#
'''
^Cheader: 
  seq: 694427
  stamp: 
    secs: 1541627323
    nsecs: 919664925
  frame_id: ''
name: [head_pan, right_j0, right_j1, right_j2, right_j3, right_j4, right_j5, right_j6, torso_t0]
position: [0.1300419921875, -0.22465625, -0.01221875, -1.4540478515625, 1.400333984375, 1.576900390625, -0.22865625, 3.1432646484375, 0.0]
velocity: [-0.001, -0.001, -0.001, -0.001, -0.001, -0.001, -0.001, -0.001, 0.0]
effort: [0.052, -0.212, -34.064, -14.176, -1.964, 2.708, -0.52, 0.324, 0.0]
---
'''
import argparse
import numpy as np

import cv2
from cv_bridge import CvBridge, CvBridgeError

import rospy
import intera_interface

def show_image_callback(img_data):
    """The callback function to show image by using CvBridge and cv
    """
    bridge = CvBridge()
    try:
        cv_image = bridge.imgmsg_to_cv2(img_data, "bgr8")
    except CvBridgeError, err:
        rospy.logerr(err)
        return
    height, width , depth  = cv_image.shape
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    cv_copy  = cv_image.copy() 

    thresholded = 0

    thresholded = cv2.erode(gray, np.ones((3,3), np.uint8), iterations=1)
    thresholded = cv2.dilate(thresholded, np.ones((3,3), np.uint8), iterations=1)

    thresholded = cv2.dilate(thresholded, np.ones((3,3), np.uint8), iterations=1)
    thresholded = cv2.erode(thresholded, np.ones((3,3), np.uint8), iterations=1)

    ret, thresh = cv2.threshold(thresholded, 20,0 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(cv_copy, contours, -1, (0,255,0),3)
    cv2.imshow('draw contours',cv_copy)

    cv_win_name = 'Sawyer'
    cv2.namedWindow(cv_win_name, 0)
    # refresh the image on the screen
    cv2.imshow(cv_win_name, cv_image)
    cv2.waitKey(3)

def main():
    """Camera Display Example

    Cognex Hand Camera Ranges
        - exposure: [0.01-100]
        - gain: [0-255]
    Head Camera Ranges:
        - exposure: [0-100], -1 for auto-exposure
        - gain: [0-79], -1 for auto-gain
    """
    rp = intera_interface.RobotParams()
    valid_cameras = rp.get_camera_names()
    if not valid_cameras:
        rp.log_message(("Cannot detect any camera_config"
            " parameters on this robot. Exiting."), "ERROR")
        return
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__)
    parser.add_argument(
        '-c', '--camera', type=str, default="right_hand_camera",
        choices=valid_cameras, help='Setup Camera Name for Camera Display')
    parser.add_argument(
        '-r', '--raw', action='store_true',
        help='Specify use of the raw image (unrectified) topic')
    parser.add_argument(
        '-e', '--edge', action='store_true',
        help='Streaming the Canny edge detection image')
    parser.add_argument(
        '-g', '--gain', type=int,
        help='Set gain for camera (-1 = auto)')
    parser.add_argument(
        '-x', '--exposure', type=float,
        help='Set exposure for camera (-1 = auto)')
    args = parser.parse_args(rospy.myargv()[1:])

    print("Initializing node... ")
    rospy.init_node('camera_display', anonymous=True)
    cameras = intera_interface.Cameras()
    if not cameras.verify_camera_exists(args.camera):
        rospy.logerr("Could not detect the specified camera, exiting the example.")
        return
    rospy.loginfo("Opening camera '{0}'...".format(args.camera))
    cameras.start_streaming(args.camera)
    rectify_image = not args.raw
    use_canny_edge = args.edge
    cameras.set_callback(args.camera, show_image_callback)

    # optionally set gain and exposure parameters
    if args.gain is not None:
        if cameras.set_gain(args.camera, args.gain):
            rospy.loginfo("Gain set to: {0}".format(cameras.get_gain(args.camera)))

    if args.exposure is not None:
        if cameras.set_exposure(args.camera, args.exposure):
            rospy.loginfo("Exposure set to: {0}".format(cameras.get_exposure(args.camera)))

    def clean_shutdown():
        print("Shutting down camera_display node.")
        cv2.destroyAllWindows()

    rospy.on_shutdown(clean_shutdown)
    rospy.loginfo("Camera_display node running. Ctrl-c to quit")
    rospy.spin()


if __name__ == '__main__':
    main()
