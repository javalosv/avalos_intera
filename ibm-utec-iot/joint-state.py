# *****************************************************************************
# Copyright (c) 2017 IBM Corporation and other Contributors.
# Jose Avalos modification
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
import rospy
from sensor_msgs.msg import JointState


class Msg:
    self.running_status = False
    #class set_interval():  # Timer wrapper
    #    def __init__(self, func, sec):
    #        def func_wrapper():
    #            self.t = threading.Timer(sec, func_wrapper)
    #            self.t.start()
    #            func()
    #        self.t = threading.Timer(sec, func_wrapper)
    #        self.t.start()
    #
    #    def cancel(self):
    #        self.t.cancel()
    def my_on_publish_callback():
        print("Confirmed received by WatsonIoTP")

    def callback(self,js):
        #print info.position[0]
        print "init_callback"
        state = "false"
        if self.running_status:
            state = "true"
        data = {'head_pan': js.position[0],
                'right_j0': js.position[1],
                'right_j1': js.position[2],
                'right_j2': js.position[3],
                'right_j3': js.position[4],
                'right_j4': js.position[5],
                'right_j5': js.position[6],
                'right_j6': js.position[7]}
        self.info={'info': data}
    #def publish():
            #print ('01')
            #rospy.Subscriber("/robot/joint_states", JointState, callback)
            #print ('02')
            #rospy.spin()
            #print ('02')
            #state = "false"
            #if running_status:
            #    state = "true"
            #data = {'q1': 10,#js.position[0],
            #        'q2': 10,#js.position[1],
            #        'q3': 10,#js.position[2],
            #        'q4': 10,#js.position[3],
            #        'q5': 20}
            #success = device_client.publishEvent(
            #    "joint_angle",
            #    "json",
            #    {'d': data},
            #    qos=0,
            #    on_publish=my_on_publish_callback)
            #if not success:
            #    print("Not connected to WatsonIoTP")

    def __init__(self):
        rospy.Subscriber("/robot/joint_states", JointState, self.callback)
        #publish()
        print "after_callback"
        success = device_client.publishEvent(
            "sawyer_msg",
            "json",
            self.info,
            qos=0,
            on_publish=self.my_on_publish_callback)
        if not success:
            print("Not connected to WatsonIoTP")

if __name__ == "__main__":
    try:
        device_file = "device.conf"
        device_options = ibmiotf.device.ParseConfigFile(device_file)
        device_client = ibmiotf.device.Client(device_options)
    except Exception as e:
            print("Caught exception connecting device: %s" % str(e))
            sys.exit()
    device_client.connect()
    rospy.init_node('list_js', anonymous=True)
    try:
        message = Msg()
    except rospy.ROSInterruptException:  pass 
    #device_client.commandCallback = my_command_callback
    #timeout = set_interval(publish, 1)
    print ('Press Ctrl+C to exit')
