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
# we are using spline generate by interp1d from scipy.interpolate

def main():

    try:
        rospy.init_node('avalos_limb_py')
        #Frecuency for Sawyer robot
        f=100
        rate = rospy.Rate(f)
        #Define topic
        pub = rospy.Publisher('/robot/limb/right/joint_command', JointCommand, queue_size=10)
        # Class to record
        data=Data()
        #Class limb to acces information sawyer
        limb = Limb()
        #Initial position
        limb.move_to_neutral()
        # Position init
        initial=limb.joint_angles()
        print "Posicion inicial terminada"
        #begin to record data
        data.writeon("cin_directa.txt")
        limb.move_to_joint_positions({"right_j6": 0.0,"right_j5": 0.0,"right_j4": 0.0,"right_j3": 0.0,"right_j2": 0.0,"right_j1": 0.0,"right_j0": 0.0})
        limb.move_to_joint_positions({"right_j6": initial["right_j6"],"right_j5": initial["right_j5"],"right_j4": initial["right_j4"],"right_j3": initial["right_j3"],"right_j2": initial["right_j2"],"right_j1": initial["right_j1"],"right_j0": initial["right_j0"]})
        time.sleep(1)
        data.writeoff()
        print "FINISH"
        initial=limb.joint_angles()
        p0=np.array([initial["right_j0"],initial["right_j1"],initial["right_j2"],initial["right_j3"],initial["right_j4"],initial["right_j5"],initial["right_j6"]])
        # Posiition end
        p1=[0,0,0,0,0,0,0]
        p2=p0
        # Knost vector time. We assum the process will take 10 sec

        k=np.array([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
        k_t=3*k
        k_pt=np.array([k_t[0],k_t[5],k_t[-1]])
        # Set inperpolation in linear form
        k_j0 = sp.interpolate.interp1d(k_pt, [p0[0],p1[0],p2[0]], kind='linear')(k_t)
        k_j1 = sp.interpolate.interp1d(k_pt, [p0[1],p1[1],p2[1]], kind='linear')(k_t)
        k_j2 = sp.interpolate.interp1d(k_pt, [p0[2],p1[2],p2[2]], kind='linear')(k_t)
        k_j3 = sp.interpolate.interp1d(k_pt, [p0[3],p1[3],p2[3]], kind='linear')(k_t)
        k_j4 = sp.interpolate.interp1d(k_pt, [p0[4],p1[4],p2[4]], kind='linear')(k_t)
        k_j5 = sp.interpolate.interp1d(k_pt, [p0[5],p1[5],p2[5]], kind='linear')(k_t)
        k_j6 = sp.interpolate.interp1d(k_pt, [p0[6],p1[6],p2[6]], kind='linear')(k_t)
        # Length time that will depend of frecuecy
        l = int(k_t[-1]*f)
        print "L:"
        print l
        new_t = np.linspace(k_t[0], k_t[-1], l)
        # Obtain all point following the interpolated points
        j0 = sp.interpolate.interp1d(k_t, k_j0, kind='cubic')(new_t)
        j1 = sp.interpolate.interp1d(k_t, k_j1, kind='cubic')(new_t)
        j2 = sp.interpolate.interp1d(k_t, k_j2, kind='cubic')(new_t)
        j3 = sp.interpolate.interp1d(k_t, k_j3, kind='cubic')(new_t)
        j4 = sp.interpolate.interp1d(k_t, k_j4, kind='cubic')(new_t)
        j5 = sp.interpolate.interp1d(k_t, k_j5, kind='cubic')(new_t)
        j6 = sp.interpolate.interp1d(k_t, k_j6, kind='cubic')(new_t)
        # Vector for velocity
        v_j0= np.zeros(l)
        v_j1= np.zeros(l)
        v_j2= np.zeros(l)
        v_j3= np.zeros(l)
        v_j4= np.zeros(l)
        v_j5= np.zeros(l)
        v_j6= np.zeros(l)
        # Vector for acceleration
        a_j0= np.zeros(l)
        a_j1= np.zeros(l)
        a_j2= np.zeros(l)
        a_j3= np.zeros(l)
        a_j4= np.zeros(l)
        a_j5= np.zeros(l)
        a_j6= np.zeros(l)

        # Vector for acceleration
        jk_j0= np.zeros(l)
        jk_j1= np.zeros(l)
        jk_j2= np.zeros(l)
        jk_j3= np.zeros(l)
        jk_j4= np.zeros(l)
        jk_j5= np.zeros(l)
        jk_j6= np.zeros(l)
        
        for i in xrange(l-1):
            v_j0[i]= (j0[i+1]-j0[i])*f
            v_j1[i]= (j1[i+1]-j1[i])*f
            v_j2[i]= (j2[i+1]-j2[i])*f
            v_j3[i]= (j3[i+1]-j3[i])*f
            v_j4[i]= (j4[i+1]-j4[i])*f
            v_j5[i]= (j5[i+1]-j5[i])*f
            v_j6[i]= (j6[i+1]-j6[i])*f

        v_j0[-1]=v_j0[-2]
        v_j1[-1]=v_j1[-2]
        v_j2[-1]=v_j2[-2]
        v_j3[-1]=v_j3[-2]
        v_j4[-1]=v_j4[-2]
        v_j5[-1]=v_j5[-2]
        v_j6[-1]=v_j6[-2]

        for i in xrange(l-1):
            a_j0[i]= (v_j0[i+1]-v_j0[i])*f
            a_j1[i]= (v_j1[i+1]-v_j1[i])*f
            a_j2[i]= (v_j2[i+1]-v_j2[i])*f
            a_j3[i]= (v_j3[i+1]-v_j3[i])*f
            a_j4[i]= (v_j4[i+1]-v_j4[i])*f
            a_j5[i]= (v_j5[i+1]-v_j5[i])*f
            a_j6[i]= (v_j6[i+1]-v_j6[i])*f

        a_j0[-1]=a_j0[-2]
        a_j1[-1]=a_j0[-2]
        a_j2[-1]=a_j0[-2]
        a_j3[-1]=a_j0[-2]
        a_j4[-1]=a_j0[-2]
        a_j5[-1]=a_j0[-2]
        a_j6[-1]=a_j0[-2]

        for i in xrange(l-1):
            jk_j0[i]= (a_j0[i+1]-a_j0[i])*f
            jk_j1[i]= (a_j1[i+1]-a_j1[i])*f
            jk_j2[i]= (a_j2[i+1]-a_j2[i])*f
            jk_j3[i]= (a_j3[i+1]-a_j3[i])*f
            jk_j4[i]= (a_j4[i+1]-a_j4[i])*f
            jk_j5[i]= (a_j5[i+1]-a_j5[i])*f
            jk_j6[i]= (a_j6[i+1]-a_j6[i])*f

        jk_j0[-1]=jk_j0[-2]
        jk_j1[-1]=jk_j1[-2]
        jk_j2[-1]=jk_j2[-2]
        jk_j3[-1]=jk_j3[-2]
        jk_j4[-1]=jk_j4[-2]
        jk_j5[-1]=jk_j5[-2]
        jk_j6[-1]=jk_j6[-2]


        j= np.array([j0,j1,j2,j3,j4,j5,j6])
        v= np.array([v_j0,v_j1,v_j2,v_j3,v_j4,v_j5,v_j6])
        a= np.array([a_j0,a_j1,a_j2,a_j3,a_j4,a_j5,a_j6])
        jk= np.array([jk_j0,jk_j1,jk_j2,jk_j3,jk_j4,jk_j5,jk_j6])

        save_matrix(j,"data_p.txt",f)
        save_matrix(v,"data_v.txt",f)
        save_matrix(a,"data_a.txt",f)
        save_matrix(jk,"data_y.txt",f)


        #Build message
        my_msg=JointCommand()
        # POSITION_MODE
        my_msg.mode=4
        my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]
        data.writeon("cin_trayectoria.txt")
        for i in xrange(l):
            my_msg.position=[j0[i],j1[i],j2[i],j3[i],j4[i],j5[i],j6[i]]
            my_msg.velocity=[v_j0[i],v_j1[i],v_j2[i],v_j3[i],v_j4[i],v_j5[i],v_j6[i]]
            my_msg.acceleration=[a_j0[i],a_j1[i],a_j2[i],a_j3[i],a_j4[i],a_j5[i],a_j6[i]]
            pub.publish(my_msg)
            rate.sleep()
        time.sleep(1)
        data.writeoff()
        print "Programa terminado   "

    except rospy.ROSInterruptException:
        rospy.logerr('Keyboard interrupt detected from the user.')

if __name__ == '__main__':
    main()
