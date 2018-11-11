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
# python final_directa.py joint_states:=/robot/joint_states
# rostopic echo /robot/limb/right/endpoint_state/pose

# ./intera sim 
# roslaunch sawyer_gazebo sawyer_world.launch
# roslaunch sawyer_moveit_config sawyer_moveit.launch electric_gripper:=false
# python opt_caso1.py joint_states:=/robot/joint_states
# Python 2.9


def main():
    try:
        #rospy.init_node('avalos_limb_py')   
        #moveit_commander.roscpp_initialize(sys.argv)
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
        if(True):
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
        
        neutral=[-7.343481724930712e-07,-1.1799709303615113,2.7170121530417646e-05,2.1799982536216014,-0.00023687847544184848,0.5696772114967752,3.1411912264073045]        
        base=[0.4045263671875, 0.3757021484375, -2.31678515625, 1.4790908203125, 2.14242578125, 2.1983291015625, 0.8213740234375]
        
        s6_down=[0.1123427734375, 0.398875, -2.4554755859375, 0.4891044921875, 2.4769873046875, 1.575130859375, 1.531140625]
        s6_up=[0.1613271484375, 0.3916650390625, -2.441814453125, 0.6957587890625, 2.515578125, 1.679708984375, 1.459033203125]
        
        obj_up=[-0.74389453125, 0.153580078125, -1.7190927734375, 0.7447021484375, 1.72510546875, 1.5934130859375, 0.317576171875]
        obj_down=[-0.7055927734375, 0.5030830078125, -1.7808125, 0.7994287109375, 2.0973154296875, 1.35018359375, 0.259451171875]
        
        centro=[0.0751162109375, 0.1868447265625, -1.93045703125, 1.425337890625, 1.7726181640625, 1.904037109375, 0.4765615234375]

        #points_1=path(neutral,centro,5)
        #points_2=path(centro,objeto,5)
        #points=path_full([neutral,objeto,centro,s6,centro,neutral],[5,5,5,5,5])
        
        
        #points=path_full([neutral,obj_up,obj_down,obj_up,centro,s6,centro,neutral],[3,3,3,3,3,3,3])

 
        alfa=0.5 

        p1=path_full([neutral,obj_up,obj_down],[2,3,2])
        p2=path_full([obj_down,obj_up,centro,base,s6_up,s6_down],[3,3,3,3,3,2])
        p3=path_full([s6_down,base,centro,obj_up],[3,3]) 

        opt_1=Opt_avalos(p1,f,alfa)
        opt_2=Opt_avalos(p2,f,alfa)
        opt_3=Opt_avalos(p3,f,alfa)

        v_time1=opt_1.full_time()
        v_time2=opt_2.full_time()
        v_time3=opt_3.full_time()


        
        j,v,a,jk=generate_path_cub(p1,v_time1,f)
        ext=len(j[0,:])
        #Build message
        my_msg=JointCommand()
        # POSITION_MODE
        my_msg.mode=4
        my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]

        for n in xrange(ext):
            my_msg.position=[j[0][n],j[1][n],j[2][n],j[3][n],j[4][n],j[5][n],j[6][n]]
            my_msg.velocity=[v[0][n],v[1][n],v[2][n],v[3][n],v[4][n],v[5][n],v[6][n]]
            my_msg.acceleration=[a[0][n],a[1][n],a[2][n],a[3][n],a[4][n],a[5][n],a[6][n]]
            pub.publish(my_msg)
            rate.sleep()
        
        gripper.close()
        time.sleep(1)

        j,v,a,jk=generate_path_cub(p2,v_time2,f)
        ext=len(j[0,:])
        #Build message
        my_msg=JointCommand()
        # POSITION_MODE
        my_msg.mode=4
        my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]

        for n in xrange(ext):
            my_msg.position=[j[0][n],j[1][n],j[2][n],j[3][n],j[4][n],j[5][n],j[6][n]]
            my_msg.velocity=[v[0][n],v[1][n],v[2][n],v[3][n],v[4][n],v[5][n],v[6][n]]
            my_msg.acceleration=[a[0][n],a[1][n],a[2][n],a[3][n],a[4][n],a[5][n],a[6][n]]
            pub.publish(my_msg)
            rate.sleep()

        gripper.open()

        j,v,a,jk=generate_path_cub(p3,v_time3,f)
        ext=len(j[0,:])
        #Build message
        my_msg=JointCommand()
        # POSITION_MODE
        my_msg.mode=4
        my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]

        for n in xrange(ext):
            my_msg.position=[j[0][n],j[1][n],j[2][n],j[3][n],j[4][n],j[5][n],j[6][n]]
            my_msg.velocity=[v[0][n],v[1][n],v[2][n],v[3][n],v[4][n],v[5][n],v[6][n]]
            my_msg.acceleration=[a[0][n],a[1][n],a[2][n],a[3][n],a[4][n],a[5][n],a[6][n]]
            pub.publish(my_msg)
            rate.sleep()

        

        '''
        group.clear_pose_targets()
        group.set_start_state_to_current_state()s
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
        pose_goal.position.y = 0.35
        pose_goal.position.z = 0.05

        pose_goal=Pose(Point(-0.1,0.6,0.05),Quaternion(-1,0,0,0))
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
        
        q=np.array([q0,q1,q2,q3,q4,q5,q6])
        print "q001",q0
        print q[0]
        #return 0 
        
        alfa=0.5  
        start = time.time()
        opt=Opt_avalos(q,f,alfa)
        v_time=opt.full_time()
        j,v,a,jk=generate_path_cub(q,v_time,f)
        ext=len(j[0,:])
        end = time.time()
        print('Process Time:', end-start)
        print ext
        #save_matrix(j,"data_p.txt",f)
        #save_matrix(v,"data_v.txt",f)
        #save_matrix(a,"data_a.txt",f)
        #save_matrix(jk,"data_y.txt",f)
        v_jk=sqrt(np.mean(np.square(jk)))
        print("Opt Time:",v_time)
        print("Min Time:",m_time)
        #print('Optimizacion:',opt.result())
        print('Costo Tiempo:',len(j[0])/float(100.0))
        print('Costo Jerk:', v_jk)
        
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
            #pub.publish(my_msg)
            rate.sleep()
        print("Control por trayectoria terminado.")
        time.sleep(0.25)
        #data.writeoff()
        '''
        print("Programa terminado.")

    except rospy.ROSInterruptException:
        rospy.logerr('Keyboard interrupt detected from the user.')

if __name__ == '__main__':
    main()
