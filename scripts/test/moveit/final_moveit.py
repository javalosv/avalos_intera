import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from trajectory_msgs.msg import JointTrajectoryPoint
# rosrun intera_interface enable_robot.py -e
# roslaunch sawyer_moveit_config sawyer_moveit.launch electric_gripper:=true
# roslaunch sawyer_moveit_config sawyer_moveit.launch
# python final_moveit.py joint_states:=/robot/joint_states
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
print "============ Printing robot state"
#print robot.get_current_state()
group.clear_pose_targets()
group.set_start_state_to_current_state()
# We can get the joint values from the group and adjust some of the values:
pose_goal = geometry_msgs.msg.Pose()
# Orientation
pose_goal.orientation.x = 0.00
pose_goal.orientation.y = 0.99
pose_goal.orientation.z = 0.00
pose_goal.orientation.w = 0.00
# Cartesian position
pose_goal.position.x = 0.7
pose_goal.position.y = -0.20
pose_goal.position.z = 0.5

group.set_pose_target(pose_goal)
a=group.plan()
print "Values:"
points=a.joint_trajectory.points
print len(points)
print points[0].positions[0]
#plan = group.go(wait=True)
# Calling `stop()` ensures that there is no residual movement
#group.stop()
# It is always good to clear your targets after planning with poses.
# Note: there is no equivalent function for clear_joint_value_targets()
group.clear_pose_targets()