# 0.2.0
from __future__ import division
import argparse
import rospy
import intera_interface
import intera_external_devices
import time
import numpy as np
from math import *

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy

from intera_core_msgs.msg import JointCommand
from scipy import interpolate
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.interpolate import interp1d
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


class Data():
	def __init__(self):
		self.write=False
		rospy.Subscriber("/robot/joint_states", JointState, self.talker)
		print("Init bridge")
		rate = rospy.Rate(100) # 10hz

	def talker(self,data):
		if(data.name[0]=="head_pan"):
			self.position=data.position[1:7]# extrae solo 7
			if(self.write):
				_file=open(self.file,"a")
				_file.write(str(data.position[1])+","+str(data.position[2])+","+str(data.position[3])+","\
				+str(data.position[4])+","+str(data.position[5])+","+str(data.position[6])+","+str(data.position[7])+\
				","+str(data.velocity[1])+","+str(data.velocity[2])+","+str(data.velocity[3])+","\
				+str(data.velocity[4])+","+str(data.velocity[5])+","+str(data.velocity[6])+","+str(data.velocity[7])+"\n")
				_file.close()

	def actual_joint_position(self):
		return self.position

	def writeon(self,_text):
		self.write=True
		self.file=_text
		file=open(_text,"w")
		file.close()
		return True

	def writeoff(self):
		self.write=False
		return True
