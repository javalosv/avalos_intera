import rospy
import argparse
from intera_interface import Limb
from intera_interface import CHECK_VERSION
from intera_core_msgs.msg import JointCommand
import numpy as np
import scipy as sp
from scipy.interpolate import interp1d
import time
from intera_avalos import *
import intera_interface
import intera_external_devices


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
from moveit_msgs.msg import RobotState
# rosrun intera_interface enable_robot.py -e
# roslaunch sawyer_moveit_config sawyer_moveit.launch electric_gripper:=true
# python opt_caso1.py joint_states:=/robot/joint_states
# rostopic echo /robot/limb/right/endpoint_state/pose
# Python 2.9
def main():

    try:
        #rospy.init_node('avalos_limb_py')
        
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

        #frecuency for Sawyer robot
        f=100
        rate = rospy.Rate(f)
        # add gripper
        gripper = intera_interface.Gripper('right_gripper')
        gripper.calibrate()
        gripper.open()

        moveit_robot_state = RobotState()
        joint_state = JointState()
        joint_state.header = Header()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = ['right_j0', 'right_j1', 'right_j2', 'right_j3', 'right_j4', 'right_j5', 'right_j6']

        #Define topic
        pub = rospy.Publisher('/robot/limb/right/joint_command', JointCommand, queue_size=10)
        # Class to record
        #data=Data()
        #Class limb to acces information sawyer
        limb = Limb()
        limb.move_to_neutral()
        group.clear_pose_targets()
        group.set_start_state_to_current_state()
        # We can get the joint values from the group and adjust some of the values:
        pose_goal = geometry_msgs.msg.Pose()
        # Orientation
        pose_goal.orientation.x = -1
        pose_goal.orientation.y = 0.0
        pose_goal.orientation.z = 0.0
        pose_goal.orientation.w = 0.0   
        
        q0=np.array([])
        q1=np.array([])
        q2=np.array([])
        q3=np.array([])
        q4=np.array([])
        q5=np.array([])
        q6=np.array([])

        # Cartesian position
        pose_goal.position.x = -0.1
        pose_goal.position.y = 0.6
        pose_goal.position.z = 0.05
        group.set_pose_target(pose_goal)
        a=group.plan()
        points=a.joint_trajectory.points
        n=len(points)
        joint_state.position = [points[n-1].positions[0], points[n-1].positions[1], points[n-1].positions[2], points[n-1].positions[3],points[n-1].positions[4], points[n-1].positions[5], points[n-1].positions[6]]
        moveit_robot_state.joint_state = joint_state
        group.set_start_state(moveit_robot_state)
        
        for i in range(n):
            q0=np.append(q0, points[i].positions[0])
            q1=np.append(q1, points[i].positions[1])
            q2=np.append(q2, points[i].positions[2])
            q3=np.append(q3, points[i].positions[3])
            q4=np.append(q4, points[i].positions[4])
            q5=np.append(q5, points[i].positions[5])
            q6=np.append(q6, points[i].positions[6])

        print "q000",q0

        # Cartesian position
        pose_goal.position.x = 0.43
        pose_goal.position.y = -0.4
        pose_goal.position.z = 0.2
        group.set_pose_target(pose_goal)
        a=group.plan()
        points=a.joint_trajectory.points
        n=len(points)
        joint_state.position = [points[n-1].positions[0], points[n-1].positions[1], points[n-1].positions[2], points[n-1].positions[3],points[n-1].positions[4], points[n-1].positions[5], points[n-1].positions[6]]
        moveit_robot_state.joint_state = joint_state
        group.set_start_state(moveit_robot_state)

        for i in range(n-1): # Si se repite un numero en posicion entra en un bug
            q0=np.append(q0, points[i+1].positions[0])
            q1=np.append(q1, points[i+1].positions[1])
            q2=np.append(q2, points[i+1].positions[2])
            q3=np.append(q3, points[i+1].positions[3])
            q4=np.append(q4, points[i+1].positions[4])
            q5=np.append(q5, points[i+1].positions[5])
            q6=np.append(q6, points[i+1].positions[6])
        #'''
        q=np.array([q0,q1,q2,q3,q4,q5,q6])
        print "q001",q0
        print q[0]
        #return 0 
        
        alfa=0.5  
        start = time.time()
        opt=Opt_2_avalos(q,f,alfa)
        v_time=opt.full_time()
        m_time=opt.minimal_time()
        j,v,a,jk=generate_path_cub(q,v_time,f)
        ext=len(j[0,:])
        end = time.time()
        print('Process Time:', end-start)
        print ext
        save_matrix(j,"data_p.txt",f)
        save_matrix(v,"data_v.txt",f)
        save_matrix(a,"data_a.txt",f)
        save_matrix(jk,"data_y.txt",f)
        print("Opt Time:",v_time)
        print("Min Time:",m_time)
        #print('Optimizacion:',opt.result())
        print('Costo Tiempo:',opt.value_time())
        print('Costo Jerk:',opt.value_jerk())

        # Position init
        #raw_input('Iniciar_CT_initial_position?')
        #limb.move_to_joint_positions({"right_j6": ik1[6],"right_j5": ik1[5], "right_j4": ik1[4], "right_j3": ik1[3], "right_j2":
        #ik1[2],"right_j1": ik1[1],"right_j0": ik1[0]})
        raw_input('Iniciar_CT_execute?')
        #Build message
        my_msg=JointCommand()
        # POSITION_MODE
        my_msg.mode=4
        my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]
        #data.writeon(str(alfa)+"trayectoria.txt")
        print("Control por trayectoria iniciado.")
        #time.sleep(0.25)
        for n in xrange(ext):
            my_msg.position=[j[0][n],j[1][n],j[2][n],j[3][n],j[4][n],j[5][n],j[6][n]]
            my_msg.velocity=[v[0][n],v[1][n],v[2][n],v[3][n],v[4][n],v[5][n],v[6][n]]
            my_msg.acceleration=[a[0][n],a[1][n],a[2][n],a[3][n],a[4][n],a[5][n],a[6][n]]
            pub.publish(my_msg)
            rate.sleep()
        print("Control por trayectoria terminado.")
        time.sleep(0.25)
        #data.writeoff()
        print("Programa terminado.")

    except rospy.ROSInterruptException:
        rospy.logerr('Keyboard interrupt detected from the user.')

if __name__ == '__main__':
    main()
