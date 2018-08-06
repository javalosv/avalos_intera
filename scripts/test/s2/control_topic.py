import rospy
import argparse
from intera_interface import Limb
from intera_interface import CHECK_VERSION
from intera_core_msgs.msg import JointCommand
import time

def main():

    try:
        rospy.init_node('avalos_limb_py')
        rate = rospy.Rate(100)
        pub = rospy.Publisher('/robot/limb/right/joint_command', JointCommand, queue_size=10)

        #limb = Limb()

        my_msg=JointCommand()
        # POSITION_MODE
        my_msg.mode=1
        my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]
        my_msg.position=[0,0,0,0,0,0,0]

        for x in xrange(100):
            pub.publish(my_msg)
            rate.sleep()

        print "Move ok"

    except rospy.ROSInterruptException:
        rospy.logerr('Keyboard interrupt detected from the user.')

if __name__ == '__main__':
    main()
