#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from avalos_intera.msg import robot_q

class Bridge:
    def __init__(self):
        rospy.Subscriber("/robot/joint_states", JointState, callback)

    def talker():
        """
        pub = rospy.Publisher('chatter', String, queue_size=10)
        rate = rospy.Rate(2) # 10hz
        while not rospy.is_shutdown():
            hello_str = "hello world %s" % rospy.get_time()
            rospy.loginfo(hello_str)
            pub.publish(hello_str)
            rate.sleep()
        """
if __name__ == '__main__':
    try:
        rospy.init_node('talker', anonymous=True)
    except rospy.ROSInterruptException:
        pass
    bridge=Bridge()