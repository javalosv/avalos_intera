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
# rosrun intera_interface enable_robot.py -e
# roslaunch sawyer_moveit_config sawyer_moveit.launch electric_gripper:=true
# python opt_caso1.py joint_states:=/robot/joint_states
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
        # Cartesian position
        pose_goal.position.x = 0.7
        pose_goal.position.y = -0.1
        pose_goal.position.z = -0.05

        group.set_pose_target(pose_goal)
        a=group.plan()
        print "Values:"
        points=a.joint_trajectory.points
        n_points = len(points)
        print n_points

        #Initial position
        k_j0 = np.zeros(n_points)
        k_j1 = np.zeros(n_points)
        k_j2 = np.zeros(n_points)
        k_j3 = np.zeros(n_points)
        k_j4 = np.zeros(n_points)
        k_j5 = np.zeros(n_points)
        k_j6 = np.zeros(n_points)

        for i in range(n_points):
            k_j0[i]=points[i].positions[0]
            k_j1[i]=points[i].positions[1]
            k_j2[i]=points[i].positions[2]
            k_j3[i]=points[i].positions[3]
            k_j4[i]=points[i].positions[4]
            k_j5[i]=points[i].positions[5]
            k_j6[i]=points[i].positions[6]

        q=np.array([k_j0,k_j1,k_j2,k_j3,k_j4,k_j5,k_j6])
        print q
        alfa=0.75  
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
