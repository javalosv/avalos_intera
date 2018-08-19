import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# roslaunch sawyer_moveit_config sawyer_moveit.launch
# python moveit.py joint_states:=/robot/joint_states
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial',anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()

group_name = 'right_arm'
group = moveit_commander.MoveGroupCommander(group_name)

display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                               moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=20)
Z= np.array([[2.5,0],[1,3],[1,7],[0,14],[1,18],[3,20],[5,21],[19,21],[20,22],[21.5,26],[22,30],[23,34],[23.5,37],[24.5,34],[25,34],[26.5,37],[26.5,34],[27,32.5],[28,32],[29,31],[29,30],[27,29],[25.2,29],[24.8,27],[25.5,24],[26,20],[26,16],[23,11],[18,9],[18,2.5],[18.5,0],[16,0],[15,2.5],[15,10],[13,9],[9,10],[8.5,6],[9,2.5],[10,0],[7.5,0],[6.5,3],[5,10],[4,10],[3.5,6],[4,2],[5,0],[2.5,0]])
scale=0.01
x= scale*Z[:,0]
y= scale*Z[:,1]
l=len(x)

tck, u = interpolate.splprep([x,y], s=0, per=True)
out = interpolate.splev(np.linspace(0, 1, 150), tck)

waypoints = []
wpose = group.get_current_pose().pose
waypoints.append(copy.deepcopy(wpose))
x_ref=0.2
y_ref=-0.15
for n in range(5):
	wpose.position.x= x_ref+out[0][n]  # Second move forward/backwards in (x)
	wpose.position.y= y_ref+out[0][n]  # Second move forward/backwards in (y)
	wpose.position.z= 0.15  # Second move forward/backwards in (y)
	wpose.orientation.x=1.0
	wpose.orientation.y=0.0
	wpose.orientation.z=0.0
	wpose.orientation.w=0.0

	waypoints.append(copy.deepcopy(wpose))
print waypoints
print "Begin calculation"
# We want the Cartesian path to be interpolated at a resolution of 1 cm
# which is why we will specify 0.01 as the eef_step in Cartesian
# translation.  We will disable the jump threshold by setting it to 0.0 disabling:
(plan, fraction) = group.compute_cartesian_path(
                                   waypoints,   # waypoints to follow
                                   0.01,        # eef_step
                                   0.0)         # jump_threshold
print "end calculation"
group.execute(plan)
# Note: We are just planning, not asking move_group to actually move the robot yet:
# return plan, fraction
