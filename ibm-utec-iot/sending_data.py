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
import argparse
from intera_interface import Limb
import rospy
from std_msgs.msg import String


running_status = True

def my_on_publish_callback():
    print("Confirmed received by WatsonIoTP")

def sendIOT():
    #rospy.init_node('avalos_limb_py')
    
    while not rospy.is_shutdown():
        limb = Limb()
        j_p=limb.joint_angles()
        j_v=limb.joint_velocities()
        p_p=limb.endpoint_pose()
        v_p=limb.endpoint_velocity()

        if running_status:
            joint_p = {'right_j0': j_p['right_j0'],
                    'right_j1': j_p['right_j1'],
                    'right_j2': j_p['right_j2'],
                    'right_j3': j_p['right_j3'],
                    'right_j4': j_p['right_j4'],
                    'right_j5': j_p['right_j5'],
                    'right_j6': j_p['right_j6']}
            joint_v = {'right_j0': j_v['right_j0'],
                    'right_j1': j_v['right_j1'],
                    'right_j2': j_v['right_j2'],
                    'right_j3': j_v['right_j3'],
                    'right_j4': j_v['right_j4'],
                    'right_j5': j_v['right_j5'],
                    'right_j6': j_v['right_j6']}
            success = device_client.publishEvent(
                "joint_angle",
                "json",
                {'j_p': joint_p,'j_v': joint_v},
                qos=0,
                on_publish=my_on_publish_callback())
            #print data  
            time.sleep(0.1)
            if not success:
                print("Not connected to WatsonIoTP")

    

if __name__ == "__main__":
    try:
        device_file = "device.conf"
        device_options = ibmiotf.device.ParseConfigFile(device_file)
        device_client = ibmiotf.device.Client(device_options)
        device_client.connect()
        rospy.init_node('listener', anonymous=True)
        sendIOT()
    except Exception as e:
        print("Caught exception connecting device: %s" % str(e))
        sys.exit()

    
    #device_client.commandCallback = my_command_callback
    #timeout = set_interval(publish, 0.3)
    #print ('Press Ctrl+C to exit')
