#!/usr/bin/env python
import rospy
from sensor_msgs.msg import JointState

def callback(data):
    print data.name
    print data.position[0]
    print data.velocity

def listener():

    rospy.init_node('listener-joint-state', anonymous=True)
    rospy.Subscriber("/robot/joint_states", JointState, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()