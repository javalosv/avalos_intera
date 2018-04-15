#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from avalos_intera.msg import robot_q
from sensor_msgs.msg import JointState

class Bridge:
    def __init__(self):
        self.pub_msg=robot_q()
        rospy.Subscriber("/robot/joint_states", JointState, self.talker)
        pub = rospy.Publisher('avalos/iot/values_q', robot_q, queue_size=10)
        print("Init bridge")
        rate = rospy.Rate(2) # 10hz
        while not rospy.is_shutdown():
            pub.publish(self.pub_msg)
            rate.sleep()
    
    def talker(self,d):            
        self.pub_msg.name=[d.name[0],d.name[1],d.name[2],d.name[3],d.name[4],d.name[5],d.name[6],d.name[7]]
        self.pub_msg.angle=[d.position[0],d.position[1],d.position[2],d.position[3],d.position[4],d.position[5],d.position[6],d.position[7]]

if __name__ == '__main__':
    
    try:
        rospy.init_node('node_q', anonymous=True)
        bridge=Bridge()
        print("Enabling robot... ")
    except rospy.ROSInterruptException:
        pass
    