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

# Python 3.5
def main():

    try:
        rospy.init_node('avalos_limb_py')
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
        data=Data()
        #Class limb to acces information sawyer
        limb = Limb()
        #Initial position
        limb.move_to_neutral()
        ik_pose_1=np.array([0.45,0.70,-0.2,0.70,0.0,0.70,0.0])
        ik1=np.array([ 0.69514791 , 0.64707899  ,1.92295654 , 0.01856896, -0.96413306, -0.92232169 , 4.16828131 ])
        ik_pose_2=np.array([0.80,0.30,0.3,0.70,0.0,0.70,0.0])
        ik2=np.array([5.97103602e-01 , -9.58042104e-02 ,  1.70891311e+00,  -9.48490850e-01,   -1.16882802e-03,   3.46304028e-01,   3.15488999e+00])
        ik_pose_3=np.array([0.50,0.00,0.65,0.70,0.0,0.70,0.0])
        ik3=np.array([ 0.63314606 ,-0.74365565,  1.14243681, -1.8618414,  -0.84360096,  1.44537886 , 3.41899404])
        ik_pose_4=np.array([0.80,-0.30,0.3,0.70,0.0,0.70,0.0])
        ik4=np.array([-0.31256034, -0.32949631,  2.12830197, -1.18751871, -0.45027567 , 1.32627167,  2.95775708])
        ik_pose_5=np.array([0.45,-0.70,-0.20,0.70,0.0,0.70,0.0])
        ik5=np.array([-1.55624859,  0.70439442,  2.52311113 ,-0.08708148 ,-0.94109983,  1.61554785  ,2.54289819])

        #ik_service_client_full(ik_pose_1)
        #ik_service_client_full(ik_pose_2)
        #ik_service_client_full(ik_pose_3)
        #ik_service_client_full(ik_pose_4)
        #ik_service_client_full(ik_pose_5)




        #initial=limb.joint_angles()
        # Define KNOTS. Set inperpolation in linear form
        limb.move_to_joint_positions({"right_j6": ik1[6],"right_j5": ik1[5], "right_j4": ik1[4], "right_j3": ik1[3], "right_j2":
        ik1[2],"right_j1": ik1[1],"right_j0": ik1[0]})

        q=np.array([[ik1[0],ik2[0],ik3[0],ik4[0],ik5[0]], \
                [ik1[1],ik2[1],ik3[1],ik4[1],ik5[1]], \
                [ik1[2],ik2[2],ik3[2],ik4[2],ik5[2]], \
                [ik1[3],ik2[3],ik3[3],ik4[3],ik5[3]], \
                [ik1[4],ik2[4],ik3[4],ik4[4],ik5[4]], \
                [ik1[5],ik2[5],ik3[5],ik4[5],ik5[5]], \
                [ik1[6],ik2[6],ik3[6],ik4[6],ik5[6]] \
                ])

        t_min, t_min_tiempo=min_time(q)
        print t_min_tiempo
        tasa=1/0.2
        knots_sec=np.round(t_min*tasa,0)
        t_k2=np.arange(knots_sec[-1])
        k_j0 = sp.interpolate.interp1d(knots_sec, [ik1[0],ik2[0],ik3[0],ik4[0],ik5[0]], kind='linear')(t_k2)
        k_j1 = sp.interpolate.interp1d(knots_sec, [ik1[1],ik2[1],ik3[1],ik4[1],ik5[1]], kind='linear')(t_k2)
        k_j2 = sp.interpolate.interp1d(knots_sec, [ik1[2],ik2[2],ik3[2],ik4[2],ik5[2]], kind='linear')(t_k2)
        k_j3 = sp.interpolate.interp1d(knots_sec, [ik1[3],ik2[3],ik3[3],ik4[3],ik5[3]], kind='linear')(t_k2)
        k_j4 = sp.interpolate.interp1d(knots_sec, [ik1[4],ik2[4],ik3[4],ik4[4],ik5[4]], kind='linear')(t_k2)
        k_j5 = sp.interpolate.interp1d(knots_sec, [ik1[5],ik2[5],ik3[5],ik4[5],ik5[5]], kind='linear')(t_k2)
        k_j6 = sp.interpolate.interp1d(knots_sec, [ik1[6],ik2[6],ik3[6],ik4[6],ik5[6]], kind='linear')(t_k2)
        q=np.array([k_j0,k_j1,k_j2,k_j3,k_j4,k_j5,k_j6])


        alfa=0.15    
        start = time.time()
        opt=Opt_2_avalos(q,f,alfa)
        v_time=opt.full_time()
        j,v,a,jk=generate_path_cub(q,v_time,f)
        ext=len(j[0,:])
        end = time.time()
        print('Process Time:', end-start)
        print ext
        save_matrix(j,"data_p.txt",f)
        save_matrix(v,"data_v.txt",f)
        save_matrix(a,"data_a.txt",f)
        save_matrix(jk,"data_y.txt",f)
        print("Vector Time",v_time)
        #print('Optimizacion:',opt.result())
        print('Costo Tiempo:',opt.value_time())
        print('Costo Jerk:',opt.value_jerk())

        # Position init
        limb.move_to_joint_positions({"right_j6": ik1[6],"right_j5": ik1[5], "right_j4": ik1[4], "right_j3": ik1[3], "right_j2":
        ik1[2],"right_j1": ik1[1],"right_j0": ik1[0]})
        #raw_input('Cerrar?')
        #time.sleep(4)
        #gripper.close()

        '''
        raw_input('Iniciar_CD?')
        data.writeon("directa.txt")
        #time.sleep(0.25)
        limb.move_to_joint_positions({"right_j6": ik2[6],"right_j5": ik2[5], "right_j4": ik2[4], "right_j3": ik2[3], "right_j2": ik2[2],"right_j1": ik2[1],"right_j0": ik2[0]})
        #raw_input('Continuar?')
        limb.move_to_joint_positions({"right_j6": ik3[6],"right_j5": ik3[5], "right_j4": ik3[4], "right_j3": ik3[3], "right_j2": ik3[2],"right_j1": ik3[1],"right_j0": ik3[0]})
        #raw_input('Continuar?')
        limb.move_to_joint_positions({"right_j6": ik4[6],"right_j5": ik4[5], "right_j4": ik4[4], "right_j3": ik4[3], "right_j2": ik4[2],"right_j1": ik4[1],"right_j0": ik4[0]})
        #raw_input('Continuar?')
        limb.move_to_joint_positions({"right_j6": ik5[6],"right_j5": ik5[5], "right_j4": ik5[4], "right_j3": ik5[3], "right_j2": ik5[2],"right_j1": ik5[1],"right_j0": ik5[0]})
        time.sleep(0.25)
        data.writeoff()
        print("Control por cinematica directa terminado.")
        '''

        raw_input('Iniciar_CT_initial_position?')
        limb.move_to_joint_positions({"right_j6": ik1[6],"right_j5": ik1[5], "right_j4": ik1[4], "right_j3": ik1[3], "right_j2":
        ik1[2],"right_j1": ik1[1],"right_j0": ik1[0]})
        raw_input('Iniciar_CT_execute?')
        #Build message
        my_msg=JointCommand()
        # POSITION_MODE
        my_msg.mode=4
        my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]
        data.writeon(str(alfa)+"trayectoria.txt")
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
        data.writeoff()
        print("Programa terminado.")

    except rospy.ROSInterruptException:
        rospy.logerr('Keyboard interrupt detected from the user.')

if __name__ == '__main__':
    main()
