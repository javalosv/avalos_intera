import argparse
import rospy
import intera_interface
import intera_external_devices
from intera_interface import CHECK_VERSION
from intera_core_msgs.msg import JointCommand
import time

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Header
from sensor_msgs.msg import JointState
from intera_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)



def record():
	file2write=open("filename",'w')
	




	file2write.write("here goes the data")
	file2write.close()


def main():

    print("Initializing node... ")
    rospy.init_node("sdk_joint_record_data")
    print("Getting robot state... ")
    rs = intera_interface.RobotEnable(CHECK_VERSION)
    print rs.version_check()
    init_state = rs.state().enabled
    rate = rospy.Rate(100) # hz
    rospy.loginfo("Enabling robot...")
    rs.enable()
    record()  
    print("Done.")


if __name__ == '__main__':
    main()

