#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
#from avalos_intera.msg import robot_q
from sensor_msgs.msg import JointState

class Bridge:
    def __init__(self):
    	file=open("data_recibed_6_58_07_07.txt","w")
    	file.close()
        rospy.Subscriber("/robot/joint_states", JointState, self.talker)
        print("Init bridge")
        rate = rospy.Rate(100) # 10hz
        while not rospy.is_shutdown():
            rate.sleep()


    def talker(self,data):            
        if(data.name[0]=="head_pan"):
        	_file=open("data_recibed_6_58_07_07.txt","a")
    		_file.write(str(data.header.stamp.secs)+str(data.header.stamp.nsecs)+","+str(data.position[1])+","+str(data.position[2])+","+str(data.position[3])+","\
    		+str(data.position[4])+","+str(data.position[5])+","+str(data.position[6])+","+str(data.position[7])+"\n")
    		_file.close()
        	
    		
#file2write.write(str(data.position[1])+' , '+str(data.position[2])+' , '+str(data.position[3])+' , '+str(data.position[4])+' , ')
    		

        #self.pub_msg.name=[d.name[0],d.name[1],d.name[2],d.name[3],d.name[4],d.name[5],d.name[6],d.name[7]]
        #self.pub_msg.angle=[d.position[0],d.position[1],d.position[2],d.position[3],d.position[4],d.position[5],d.position[6],d.position[7]]


def main():
	try:
		rospy.init_node('node_q', anonymous=True)
		bridge=Bridge()
		print("Enabling robot... ")
	except rospy.ROSInterruptException:
		pass

if __name__ == '__main__':
    
    main()