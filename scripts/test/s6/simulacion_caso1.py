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

# Python 3.5
def main():



    #frecuency for Sawyer robot
    f=100
    #Initial position
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

    alfa=[0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95]
    l_alfa=len(alfa)
    v_t=np.ones(l_alfa)
    v_jk=np.ones(l_alfa)
    t_p=np.ones(l_alfa)
    for i in xrange(l_alfa):
        print "------------------------------------------------"
        start = time.time()
        opt=Opt_2_avalos(q,f,alfa[i])
        v_time=opt.full_time()
        end = time.time()
        t_p[i]=end-start
        print 'Process Time:', t_p[i]
        v_t[i]=opt.value_time()
        v_jk[i]=opt.value_jerk()
        print 'k:',opt.result()
        print 'Costo Tiempo:',v_t[i]
        print 'Costo Jerk:',v_jk[i]
        j,v,a,jk=generate_path_cub(q,v_time,f)
        save_matrix(j,str(alfa[i])+"_data_p.txt",f)
        save_matrix(v,str(alfa[i])+"_data_v.txt",f)
        save_matrix(a,str(alfa[i])+"_data_a.txt",f)
        save_matrix(jk,str(alfa[i])+"_data_y.txt",f)
        print v_time
    raw_data = {'alfa':alfa,
    'time':t_p,
    'v_t':v_t,
    'v_jk':v_jk
    }
    df = pd.DataFrame(raw_data)
    df.to_csv('example.csv')
    #plt.plot(v_t,v_jk,'r*',v_t,v_jk,)
    #plt.xlabel("Variable_tiempo")
    #plt.ylabel("Variable_jerk")
    #plt.show()
    print "Programa terminado."


if __name__ == '__main__':
    main()
