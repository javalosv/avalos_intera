import rospy
import argparse
from intera_interface import Limb
from intera_interface import CHECK_VERSION
from intera_core_msgs.msg import JointCommand
import numpy as np
import scipy as sp
import math
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
# python opt_caso2.py joint_states:=/robot/joint_states
# rostopic echo /robot/limb/right/endpoint_state/pose
# Python 2.9

def main():

    try:
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('avalos_limb_py',anonymous=True)
        robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()
        group_name = 'right_arm'
        group = moveit_commander.MoveGroupCommander(group_name)

        #frecuency for Sawyer robot
        f=100
        alfa=0.9
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
        limb = Limb()
        limb.move_to_neutral()
        limb.move_to_joint_positions({"right_j6":2})
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

        

        # Cartesian position - Carga '01'
        pose_goal.position.x = 0.758552
        pose_goal.position.y = -0.3435
        pose_goal.position.z = 0.25
        group.set_pose_target(pose_goal)
        carga1=group.plan().joint_trajectory.points
        n=len(carga1)
        joint_state.position = [carga1[-1].positions[0], carga1[-1].positions[1], carga1[-1].positions[2], carga1[-1].positions[3],carga1[-1].positions[4], carga1[-1].positions[5], carga1[-1].positions[6]]
        moveit_robot_state.joint_state = joint_state
        group.set_start_state(moveit_robot_state)
        

        tmp=np.array([])
        
        if(n>8):
            tmp=np.append(tmp,0)
            k=int(math.sqrt(n)+2)
            r=int((n-1)/float(k))
            for i in range(k):
                print i
                tmp=np.append(tmp,int(r*(i+1)-1))
            tmp=np.append(tmp,n-1)
        else:
            for i in range(n):
                print i
                tmp=np.append(tmp,i)

        print "tmp:", tmp
        for i in range(len(tmp)):
            q0=np.append(q0, carga1[int(tmp[i])].positions[0])
            q1=np.append(q1, carga1[int(tmp[i])].positions[1])
            q2=np.append(q2, carga1[int(tmp[i])].positions[2])
            q3=np.append(q3, carga1[int(tmp[i])].positions[3])
            q4=np.append(q4, carga1[int(tmp[i])].positions[4])
            q5=np.append(q5, carga1[int(tmp[i])].positions[5])
            q6=np.append(q6, carga1[int(tmp[i])].positions[6])

        print "q000",q0

        # Cartesian position - Carga '00'
        #pose_goal.position.x = 0.85
        #pose_goal.position.y = -0.4
        pose_goal.position.z = -0.01

        
        group.set_pose_target(pose_goal)
        carga0=group.plan().joint_trajectory.points
     
        q0=np.append(q0, carga0[-1].positions[0])
        q1=np.append(q1, carga0[-1].positions[1])
        q2=np.append(q2, carga0[-1].positions[2])
        q3=np.append(q3, carga0[-1].positions[3])
        q4=np.append(q4, carga0[-1].positions[4])
        q5=np.append(q5, carga0[-1].positions[5])
        q6=np.append(q6, carga0[-1].positions[6])
        #'''
        q=np.array([q0,q1,q2,q3,q4,q5,q6])
        print "q001",q0

        m_time, t_min_tiempo=min_time(q)
        
        start = time.time()
        opt=Opt_avalos(q,f,0.9)
        v_time=opt.full_time()
        j_1,v_1,a_1,jk_1=generate_path_cub(q,v_time,f)
        ext_1=len(j_1[0,:])
        end = time.time()
        print('Process Time:', end-start)
        v_jk=sqrt(np.mean(np.square(jk_1)))
        print("Opt Time:",v_time)
        print("Min Time:",m_time)
        #print('Optimizacion:',opt.result())
        max_v=np.amax(np.absolute(v_1))
        max_ac=np.amax(np.absolute(a_1))
        max_jk=np.amax(np.absolute(jk_1))
        print "Max Velo:",max_v
        print "Max Acel:",max_ac
        print "Max Jerk:",max_jk
        #raw_input('Iniciar_CT_execute?')
        #Build message
        my_msg=JointCommand()
        # POSITION_MODE
        my_msg.mode=4
        my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5"]#,"right_j6"]
        print("Control por trayectoria iniciado.")
        #time.sleep(0.25)
        

        q0=np.array([])
        q1=np.array([])
        q2=np.array([])
        q3=np.array([])
        q4=np.array([])
        q5=np.array([])
        q6=np.array([])

        q0=np.append(q0, carga0[-1].positions[0])
        q1=np.append(q1, carga0[-1].positions[1])
        q2=np.append(q2, carga0[-1].positions[2])
        q3=np.append(q3, carga0[-1].positions[3])
        q4=np.append(q4, carga0[-1].positions[4])
        q5=np.append(q5, carga0[-1].positions[5])
        q6=np.append(q6, carga0[-1].positions[6])



        joint_state.position = [carga1[-1].positions[0], carga1[-1].positions[1], carga1[-1].positions[2], carga1[-1].positions[3],carga1[-1].positions[4], carga1[-1].positions[5], carga1[-1].positions[6]]
        moveit_robot_state.joint_state = joint_state
        group.set_start_state(moveit_robot_state)

        # Cartesian position - Base '01'
        pose_goal.position.x = 0.80791
        pose_goal.position.y = 0.4461
        pose_goal.position.z = 0.2501
        group.set_pose_target(pose_goal)

        base1=group.plan().joint_trajectory.points
        n=len(base1)
        joint_state.position = [base1[-1].positions[0], base1[-1].positions[1], base1[-1].positions[2], base1[-1].positions[3],base1[-1].positions[4], base1[-1].positions[5], base1[-1].positions[6]]
        moveit_robot_state.joint_state = joint_state
        group.set_start_state(moveit_robot_state)


        tmp=np.array([])
        
        if(n>14):
            tmp=np.append(tmp,0)
            k=int(math.sqrt(n)+3)
            r=int((n-1)/float(k))
            for i in range(k):
                print i
                tmp=np.append(tmp,int(r*(i+1)-1))
            tmp=np.append(tmp,n-1)
        else:
            for i in range(n):
                print i
                tmp=np.append(tmp,i)

        print "tmp:", tmp
        for i in range(len(tmp)):
            q0=np.append(q0, base1[int(tmp[i])].positions[0])
            q1=np.append(q1, base1[int(tmp[i])].positions[1])
            q2=np.append(q2, base1[int(tmp[i])].positions[2])
            q3=np.append(q3, base1[int(tmp[i])].positions[3])
            q4=np.append(q4, base1[int(tmp[i])].positions[4])
            q5=np.append(q5, base1[int(tmp[i])].positions[5])
            q6=np.append(q6, base1[int(tmp[i])].positions[6])

        print "q000",q0

        # Cartesian position - Base '00'
        #pose_goal.position.x = 0.90
        #pose_goal.position.y = 0.38
        pose_goal.position.z = 0.01

        
        group.set_pose_target(pose_goal)
        base0=group.plan().joint_trajectory.points
     
        q0=np.append(q0, base0[-1].positions[0])
        q1=np.append(q1, base0[-1].positions[1])
        q2=np.append(q2, base0[-1].positions[2])
        q3=np.append(q3, base0[-1].positions[3])
        q4=np.append(q4, base0[-1].positions[4])
        q5=np.append(q5, base0[-1].positions[5])
        q6=np.append(q6, base0[-1].positions[6])

        q=np.array([q0,q1,q2,q3,q4,q5,q6])
        print "q001",q0
        #print q[0]
        #return 0 
        m_time, t_min_tiempo=min_time(q) 
        start = time.time()
        opt=Opt_avalos(q,f,alfa)
        v_time=opt.full_time()
        j_2,v_2,a_2,jk_2=generate_path_cub(q,v_time,f)
        ext_2=len(j_2[0,:])
        end = time.time()
        print('Process Time:', end-start)
        #save_matrix(j,"data_p.txt",f)
        #save_matrix(v,"data_v.txt",f)
        #save_matrix(a,"data_a.txt",f)
        #save_matrix(jk,"data_y.txt",f)
        v_jk=sqrt(np.mean(np.square(jk_2)))
        print("Opt Time:",v_time)
        print("Min Time:",m_time)
        #print('Optimizacion:',opt.result())
        max_v=np.amax(np.absolute(v_2))
        max_ac=np.amax(np.absolute(a_2))
        max_jk=np.amax(np.absolute(jk_2))
        print "Max Velo:",max_v
        print "Max Acel:",max_ac
        print "Max Jerk:",max_jk


        q0=np.array([])
        q1=np.array([])
        q2=np.array([])
        q3=np.array([])
        q4=np.array([])
        q5=np.array([])
        q6=np.array([])

        q0=np.append(q0, base0[-1].positions[0])
        q1=np.append(q1, base0[-1].positions[1])
        q2=np.append(q2, base0[-1].positions[2])
        q3=np.append(q3, base0[-1].positions[3])
        q4=np.append(q4, base0[-1].positions[4])
        q5=np.append(q5, base0[-1].positions[5])
        q6=np.append(q6, base0[-1].positions[6])

        # Cartesian position - Carga '01'
        pose_goal.position.x = 0.7708552
        pose_goal.position.y = -0.394135
        pose_goal.position.z = 0.24
        group.set_pose_target(pose_goal)
        carga1=group.plan().joint_trajectory.points
        n=len(carga1)
                

        tmp=np.array([])
        
        if(n>10):
            tmp=np.append(tmp,0)
            k=int(math.sqrt(n)+2)
            r=int((n-1)/float(k))
            for i in range(k):
                print i
                tmp=np.append(tmp,int(r*(i+1)-1))
            tmp=np.append(tmp,n-1)
        else:
            for i in range(n):
                print i
                tmp=np.append(tmp,i)

        print "tmp:", tmp
        for i in range(len(tmp)):
            q0=np.append(q0, carga1[int(tmp[i])].positions[0])
            q1=np.append(q1, carga1[int(tmp[i])].positions[1])
            q2=np.append(q2, carga1[int(tmp[i])].positions[2])
            q3=np.append(q3, carga1[int(tmp[i])].positions[3])
            q4=np.append(q4, carga1[int(tmp[i])].positions[4])
            q5=np.append(q5, carga1[int(tmp[i])].positions[5])
            q6=np.append(q6, carga1[int(tmp[i])].positions[6])

        q=np.array([q0,q1,q2,q3,q4,q5,q6])
        print "q001",q0
        #print q[0]
        #return 0 
        m_time, t_min_tiempo=min_time(q) 
        start = time.time()
        opt=Opt_avalos(q,f,0.8)
        v_time=opt.full_time()
        j_3,v_3,a_3,jk_3=generate_path_cub(q,v_time,f)
        ext_3=len(j_3[0,:])
        end = time.time()
        print('Process Time:', end-start)
        #save_matrix(j,"data_p.txt",f)
        #save_matrix(v,"data_v.txt",f)
        #save_matrix(a,"data_a.txt",f)
        #save_matrix(jk,"data_y.txt",f)
        v_jk=sqrt(np.mean(np.square(jk_3)))
        print("Opt Time:",v_time)
        print("Min Time:",m_time)
        #print('Optimizacion:',opt.result())
        max_v=np.amax(np.absolute(v_3))
        max_ac=np.amax(np.absolute(a_3))
        max_jk=np.amax(np.absolute(jk_3))
        print "Max Velo:",max_v
        print "Max Acel:",max_ac
        print "Max Jerk:",max_jk



        raw_input('Iniciar_CT_execute?')
        #Build message
       

        for n in xrange(ext_1):
            my_msg.position=[j_1[0][n],j_1[1][n],j_1[2][n],j_1[3][n],j_1[4][n],j_1[5][n]]#,j_1[6][n]]
            my_msg.velocity=[v_1[0][n],v_1[1][n],v_1[2][n],v_1[3][n],v_1[4][n],v_1[5][n]]#,v_1[6][n]]
            my_msg.acceleration=[a_1[0][n],a_1[1][n],a_1[2][n],a_1[3][n],a_1[4][n],a_1[5][n]]#,a_1[6][n]]
            pub.publish(my_msg)
            rate.sleep()
        print("Control por trayectoria terminado.")

        time.sleep(0.25)
        gripper.close()

        print("Control por trayectoria iniciado.")
        #time.sleep(0.25)
        for n in xrange(ext_2):
            my_msg.position=[j_2[0][n],j_2[1][n],j_2[2][n],j_2[3][n],j_2[4][n],j_2[5][n]]#,j_2[6][n]]
            my_msg.velocity=[v_2[0][n],v_2[1][n],v_2[2][n],v_2[3][n],v_2[4][n],v_2[5][n]]#,v_2[6][n]]
            my_msg.acceleration=[a_2[0][n],a_2[1][n],a_2[2][n],a_2[3][n],a_2[4][n],a_2[5][n]]#,a_2[6][n]]
            pub.publish(my_msg)
            rate.sleep()
        print("Control por trayectoria terminado.")

        gripper.open()
        time.sleep(0.5)
        #data.writeoff()
        print("Programa terminado.")

        for n in xrange(ext_3):
            my_msg.position=[j_3[0][n],j_3[1][n],j_3[2][n],j_3[3][n],j_3[4][n],j_3[5][n]]#,j_3[6][n]]
            my_msg.velocity=[v_3[0][n],v_3[1][n],v_3[2][n],v_3[3][n],v_3[4][n],v_3[5][n]]#,v_3[6][n]]
            my_msg.acceleration=[a_3[0][n],a_3[1][n],a_3[2][n],a_3[3][n],a_3[4][n],a_3[5][n]]#,a_3[6][n]]
            pub.publish(my_msg)
            rate.sleep()
        print("Control por trayectoria terminado.")

        gripper.open()
        #data.writeoff()
        print("Programa terminado.")



    except rospy.ROSInterruptException:
        rospy.logerr('Keyboard interrupt detected from the user.')

if __name__ == '__main__':
    main()
