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

# This example show how the robot move from neutral position to zero position and return to neutral position
# we are using spline based on own library

def main():

    try:
        rospy.init_node('avalos_limb_py')
        #frecuency for Sawyer robot
        f=100
        rate = rospy.Rate(f)
        #Define topic
        pub = rospy.Publisher('/robot/limb/right/joint_command', JointCommand, queue_size=10)
        # Class to record
        data=Data()
        #Class limb to acces information sawyer
        limb = Limb()
        #Initial position
        #limb.move_to_neutral()
        #time.sleep(1)
        # Position init
        initial=limb.joint_angles()
        print "Posicion inicial terminada"
        #begin to record data
        data.writeon("cin_directa.txt")
        print "Control por cinematica directa iniciado."
        time.sleep(0.5)
        limb.move_to_joint_positions({"right_j6": 0.0,"right_j5": 0.0,"right_j4": 0.0,"right_j3": 0.0,"right_j2": 0.0,"right_j1": 0.0,"right_j0": 0.0})
        limb.move_to_joint_positions({"right_j6": initial["right_j6"],"right_j5": initial["right_j5"],"right_j4": initial["right_j4"],"right_j3": initial["right_j3"],"right_j2": initial["right_j2"],"right_j1": initial["right_j1"],"right_j0": initial["right_j0"]})
        time.sleep(1)
        data.writeoff()
        print "Control por cinematica directa terminado."
        initial=limb.joint_angles()
        p0=np.array([initial["right_j0"],initial["right_j1"],initial["right_j2"],initial["right_j3"],initial["right_j4"],initial["right_j5"],initial["right_j6"]])
        # Posiition end
        p1=[0,0,0,0,0,0,0]
        p2=p0
        # Knost vector time. We assum the process will take 10 sec

        k=np.array([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
        tiempo_estimado=7
        k_t=tiempo_estimado*k
        k_pt=np.array([k_t[0],k_t[5],k_t[-1]])
        # Define KNOTS. Set inperpolation in linear form
        k_j0 = sp.interpolate.interp1d(k_pt, [p0[0],p1[0],p2[0]], kind='linear')(k_t)
        k_j1 = sp.interpolate.interp1d(k_pt, [p0[1],p1[1],p2[1]], kind='linear')(k_t)
        k_j2 = sp.interpolate.interp1d(k_pt, [p0[2],p1[2],p2[2]], kind='linear')(k_t)
        k_j3 = sp.interpolate.interp1d(k_pt, [p0[3],p1[3],p2[3]], kind='linear')(k_t)
        k_j4 = sp.interpolate.interp1d(k_pt, [p0[4],p1[4],p2[4]], kind='linear')(k_t)
        k_j5 = sp.interpolate.interp1d(k_pt, [p0[5],p1[5],p2[5]], kind='linear')(k_t)
        k_j6 = sp.interpolate.interp1d(k_pt, [p0[6],p1[6],p2[6]], kind='linear')(k_t)
        q=np.array([k_j0,k_j1,k_j2,k_j3,k_j4,k_j5,k_j6])
        [t,t_rec]=min_time(q)
        print "t:"
        print t
        [j,v,a,jk,ext]=generate_path_cub(q,t,f)
        save_matrix(j,"data_p.txt",f)
        save_matrix(v,"data_v.txt",f)
        save_matrix(a,"data_a.txt",f)
        save_matrix(jk,"data_y.txt",f)

        v_t=round(6*(ext/float(f)),2)
        print "Valor tiempo: ",v_t
        print "Valor jerk", v_jk

        raw_input('Iniciar?')

        #Build message
        my_msg=JointCommand()
        # POSITION_MODE
        my_msg.mode=4
        my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]
        data.writeon("cin_trayectoria.txt")
        print "Control por trayectoria iniciado."
        time.sleep(0.5)
        for n in xrange(ext):
            my_msg.position=[j[0][n],j[1][n],j[2][n],j[3][n],j[4][n],j[5][n],j[6][n]]
            my_msg.velocity=[v[0][n],v[1][n],v[2][n],v[3][n],v[4][n],v[5][n],v[6][n]]
            my_msg.acceleration=[a[0][n],a[1][n],a[2][n],a[3][n],a[4][n],a[5][n],a[6][n]]
            pub.publish(my_msg)
            rate.sleep()
        print "Control por trayectoria terminado."
        time.sleep(1)
        data.writeoff()
        print "Programa terminado."

    except rospy.ROSInterruptException:
        rospy.logerr('Keyboard interrupt detected from the user.')

if __name__ == '__main__':
    main()
