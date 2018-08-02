import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
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
# We can get the name of the reference frame for this robot:
planning_frame = group.get_planning_frame()
print "============ Reference frame: %s" % planning_frame

# We can also print the name of the end-effector link for this group:
eef_link = group.get_end_effector_link()
print "============ End effector: %s" % eef_link

# We can get a list of all the groups in the robot:
group_names = robot.get_group_names()
print "============ Robot Groups:", robot.get_group_names()

# Sometimes for debugging it is useful to print the entire state of the
# robot:
#print "============ Printing robot state"
#print robot.get_current_state()
#print ""


# We can get the joint values from the group and adjust some of the values:
joint_goal = group.get_current_joint_values()
joint_goal[0] = -0.0000000001
joint_goal[1] = -1.0000000001
joint_goal[2] =  0.0000000001
joint_goal[3] =  1.0200000001
joint_goal[4] =  0.0000000001
joint_goal[5] =  -0
joint_goal[6] = 3.1415
#name: [head_pan, right_j0, right_j1, right_j2, right_j3, right_j4, right_j5, right_j6, torso_t0]
#position: [-0.396677734375, -0.1602412109375, -0.92309375, 0.145767578125, 1.1989
# The go command can be called with joint values, poses, or without any
# parameters if you have already set the pose or joint target for the group


a= group.plan(joint_goal)
position=a.joint_trajectory.points
print len(position) 
group.go(joint_goal, wait=True)
# Calling ``stop()`` ensures that there is no residual movement
#group.stop()
#pose_goal = geometry_msgs.msg.Pose()
#pose_goal.orientation.x = 1.0
#pose_goal.position.x = 0.8
#pose_goal.position.y = 0.1
#pose_goal.position.z = 0.0
#group.set_pose_target(pose_goal)

#a= group.plan(pose_goal)
#position=a.joint_trajectory.points
#print len(position) 

#plan = group.go(wait=True)
# Calling `stop()` ensures that there is no residual movement
#group.stop()
# It is always good to clear your targets after planning with poses.
# Note: there is no equivalent function for clear_joint_value_targets()
#group.clear_pose_targets()



