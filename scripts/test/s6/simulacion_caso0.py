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
import sys
import intera_interface
import intera_external_devices
import matplotlib.pyplot as plt
import pandas as pd
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

# Python 3.5
def main():

    try:
        #Frecuency for Sawyer robot
        f=100
        p0=[0,-1.1799,0.0,2.1799,-0.0002,0.5696,3.14119]
        p1=[0,0,0,0,0,0,0]
        p2=p0
        # Knost vector time. We assum the process will take 10 sec

        k=np.array([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
        tiempo_estimado=7
        k_t=tiempo_estimado*k
        k_pt=np.array([k_t[0],k_t[5],k_t[-1]])
        # Set inperpolation in linear form
        q0 = sp.interpolate.interp1d(k_pt, [p0[0],p1[0],p2[0]], kind='linear')(k_t)
        q1 = sp.interpolate.interp1d(k_pt, [p0[1],p1[1],p2[1]], kind='linear')(k_t)
        q2 = sp.interpolate.interp1d(k_pt, [p0[2],p1[2],p2[2]], kind='linear')(k_t)
        q3 = sp.interpolate.interp1d(k_pt, [p0[3],p1[3],p2[3]], kind='linear')(k_t)
        q4 = sp.interpolate.interp1d(k_pt, [p0[4],p1[4],p2[4]], kind='linear')(k_t)
        q5 = sp.interpolate.interp1d(k_pt, [p0[5],p1[5],p2[5]], kind='linear')(k_t)
        q6 = sp.interpolate.interp1d(k_pt, [p0[6],p1[6],p2[6]], kind='linear')(k_t)

        print k_t
        q=np.array([q0,q1,q2,q3,q4,q5,q6])

        j,v,a,jk=generate_path_cub(q,k_t,f)
        save_matrix(j,"data_p.txt",f)
        save_matrix(v,"data_v.txt",f)
        save_matrix(a,"data_a.txt",f)
        save_matrix(jk,"data_y.txt",f)

        

    except rospy.ROSInterruptException:
        rospy.logerr('Keyboard interrupt detected from the user.')

if __name__ == '__main__':
    main()

