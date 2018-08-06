import rospy
import argparse
from intera_interface import Limb
from intera_interface import CHECK_VERSION
from intera_core_msgs.msg import JointCommand
import numpy as np
import scipy as sp
from scipy.interpolate import interp1d
import time

# This example show how the robot move from neutral position to zero position
def main():

    try:
        rospy.init_node('avalos_limb_py')
        #Frecuency for Sawyer robot
        f=100
        rate = rospy.Rate(f)
        #Define topic
        pub = rospy.Publisher('/robot/limb/right/joint_command', JointCommand, queue_size=10)
        #Class limb to acces information sawyer
        limb = Limb()
        #Initial position
        limb.move_to_neutral()
        print "posicion inicial terminada"
        # Position init
        initial=limb.joint_angles()
        initial["right_j0"]
        pi=[initial["right_j0"],initial["right_j1"],initial["right_j2"],initial["right_j3"],initial["right_j4"],initial["right_j5"],initial["right_j6"]]
        # Posiition end
        pe=[0,0,0,0,0,0,0]
        # Knost vector time
        k_t=[0,1,2,3,4,5,6,7,8,9,10]
        # Set knots points for each joint
        k_j0=np.linspace(pi[0], pe[0], num=11)
        k_j1=np.linspace(pi[1], pe[1], num=11)
        k_j2=np.linspace(pi[2], pe[2], num=11)
        k_j3=np.linspace(pi[3], pe[3], num=11)
        k_j4=np.linspace(pi[4], pe[4], num=11)
        k_j5=np.linspace(pi[5], pe[5], num=11)
        k_j6=np.linspace(pi[6], pe[6], num=11)
        # Length time that will depend of frecuecy
        l = k_t[-1]*f
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
        a_j0[-2]=a_j0[-3]
        a_j1[-2]=a_j1[-3]
        a_j2[-2]=a_j2[-3]
        a_j3[-2]=a_j3[-3]
        a_j4[-2]=a_j4[-3]
        a_j5[-2]=a_j5[-3]
        a_j6[-2]=a_j6[-3]

        a_j0[-1]=a_j0[-2]
        a_j1[-1]=a_j1[-2]
        a_j2[-1]=a_j2[-2]
        a_j3[-1]=a_j3[-2]
        a_j4[-1]=a_j4[-2]
        a_j5[-1]=a_j5[-2]
        a_j6[-1]=a_j6[-2]

        #Build message
        my_msg=JointCommand()
        # POSITION_MODE
        my_msg.mode=4
        my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]

        for i in xrange(l):
            my_msg.position=[j0[i],j1[i],j2[i],j3[i],j4[i],j5[i],j6[i]]
            my_msg.velocity=[v_j0[i],v_j1[i],v_j2[i],v_j3[i],v_j4[i],v_j5[i],v_j6[i]]
            my_msg.acceleration=[a_j0[i],a_j1[i],a_j2[i],a_j3[i],a_j4[i],a_j5[i],a_j6[i]]
            pub.publish(my_msg)
            rate.sleep()

        print "Move ok"

    except rospy.ROSInterruptException:
        rospy.logerr('Keyboard interrupt detected from the user.')

if __name__ == '__main__':
    main()
