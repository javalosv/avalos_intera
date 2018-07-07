# *****************************************************************************
# Copyright (c) 2017 Jose Avalos
# *****************************************************************************
#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import getopt
import time
import sys
import uuid
import threading
import time
import signal
import os
import random
import ibmiotf.device
import math


import rospy
from std_msgs.msg import String
from avalos_intera.msg import robot_q

running_status = True

class SendIOT:
    def __init__(self):
        self.pub_msg=[0,0,0,0,0,0,0,0]
        rospy.Subscriber("avalos/iot/values_q", robot_q, self.sender)
        state = "false"
        while not rospy.is_shutdown():
            if running_status:
                state = "true"
                data = {'head_pan':self.pub_msg[0],
                        'right_j0': self.pub_msg[1],
                        'right_j1': self.pub_msg[2],
                        'right_j2': self.pub_msg[3],
                        'right_j3': self.pub_msg[4],
                        'right_j4': self.pub_msg[5],
                        'right_j5': self.pub_msg[6],
                        'right_j6': self.pub_msg[7]   }
                success = device_client.publishEvent(
                    "joint_angle",
                    "json",
                    {'d': data},
                    qos=0,
                    on_publish=self.my_on_publish_callback)
                #print data  
                time.sleep(0.3)
                if not success:
                    print("Not connected to WatsonIoTP")

    def my_on_publish_callback(self):
        print("Confirmed received by WatsonIoTP")

    def sender(self,d):
        #self.pub_msg=d.angle
        self.pub_msg[0]=round(math.degrees(d.angle[0]),2)
        self.pub_msg[1]=round(math.degrees(d.angle[1]),2)
        self.pub_msg[2]=round(math.degrees(d.angle[2]),2)
        self.pub_msg[3]=round(math.degrees(d.angle[3]),2)
        self.pub_msg[4]=round(math.degrees(d.angle[4]),2)
        self.pub_msg[5]=round(math.degrees(d.angle[5]),2)
        self.pub_msg[6]=round(math.degrees(d.angle[6]),2)
        self.pub_msg[7]=round(math.degrees(d.angle[7]),2)
        #print ("pass data")
if __name__ == "__main__":
    try:
        device_file = "device.conf"
        device_options = ibmiotf.device.ParseConfigFile(device_file)
        device_client = ibmiotf.device.Client(device_options)
        device_client.connect()
        rospy.init_node('listener', anonymous=True)
        send=SendIOT()
    except Exception as e:
        print("Caught exception connecting device: %s" % str(e))
        sys.exit()

    
    #device_client.commandCallback = my_command_callback
    #timeout = set_interval(publish, 0.3)
    #print ('Press Ctrl+C to exit')
