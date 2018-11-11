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
from intera_interface import Limb

import rospy
from std_msgs.msg import String
from avalos_intera.msg import robot_q

def inicio():
    running_status = True
    limb = Limb()
    
    state = "false"
    while not rospy.is_shutdown():
        if running_status:
            j_p=limb.joint_angles()
            state = "true"
            data = {'head_pan':round(180*j_p['right_j0']/3.14,1),
                    'right_j0':round(180*j_p['right_j0']/3.14,1),
                    'right_j1':round(180*j_p['right_j1']/3.14,1),
                    'right_j2':round(180*j_p['right_j2']/3.14,1),
                    'right_j3':round(180*j_p['right_j3']/3.14,1),
                    'right_j4':round(180*j_p['right_j4']/3.14,1),
                    'right_j5':round(180*j_p['right_j5']/3.14,1),
                    'right_j6':round(180*j_p['right_j6']/3.14,1)  }
            success = device_client.publishEvent(
                "joint_angle",
                "json",
                {'d': data},
                qos=0,
                on_publish=my_on_publish_callback)
            #print data  
            time.sleep(0.3)
            if not success:
                print("Not connected to WatsonIoTP")
def my_on_publish_callback():
    print("Confirmed received by WatsonIoTP")


if __name__ == "__main__":
    try:
        device_file = "device.conf"
        device_options = ibmiotf.device.ParseConfigFile(device_file)
        device_client = ibmiotf.device.Client(device_options)
        device_client.connect()
        rospy.init_node('listener', anonymous=True)
        inicio()
    except Exception as e:
        print("Caught exception connecting device: %s" % str(e))
        sys.exit()

    
    #device_client.commandCallback = my_command_callback
    #timeout = set_interval(publish, 0.3)
    #print ('Press Ctrl+C to exit')
