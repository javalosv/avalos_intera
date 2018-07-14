import argparse
import rospy
import intera_interface
import intera_external_devices
import time

import numpy as np

from avalos_sawyer import * 
from intera_interface import CHECK_VERSION
from intera_core_msgs.msg import JointCommand
from scipy import interpolate
from scipy.interpolate import UnivariateSpline
from scipy.interpolate import interp1d
from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)
from std_msgs.msg import Header
from sensor_msgs.msg import JointState
from intera_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)


def set_move():

    F=100   #Frecuencia de envio
    rate = rospy.Rate(F) # hz
    limb = intera_interface.Limb('right')
    limb.move_to_neutral()
    ik_service_client_full(0.662,0.450,-0.040,0.717,0,0.717,0)
    print "Posicion neutral terminada"
    time.sleep(1)
    getdata1=Getdata("IK_data.txt")
    getdata1.writeon()
    time.sleep(0.75)
    [succes,q1]=ik_service_client_full(0.662,0.450,-0.040,0.717,0,0.717,0)
    [succes,q2]=ik_service_client_full(0.662,0.200,0.290,0.717,0,0.717,0)
    [succes,q3]=ik_service_client_full(0.662,-0.150,0.290,0.717,0,0.717,0)
    [succes,q4]=ik_service_client_full(0.662,-0.450,-0.040,0.717,0,0.717,0)
    [succes,q5]=ik_service_client_full(0.662,-0.150,0.290,0.717,0,0.717,0)
    [succes,q6]=ik_service_client_full(0.662,0.200,0.290,0.717,0,0.717,0)
    [succes,q7]=ik_service_client_full(0.662,0.450,-0.040,0.717,0,0.717,0)
    time.sleep(0.75)
    getdata1.writeoff()

    # Inicia en el joint [[j0,j1,j2,j3,j4,j5,j6],[...]]
    print "Posicion inicial terminada"
    names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]   
    pub = rospy.Publisher('/robot/limb/right/joint_command', JointCommand, queue_size=10)
    q=np.matrix([q1,q2,q3,q4,q5,q6,q7])
    print q
    [t,t_rec]=opt_time(q,F)
    k=1.25  #Factor de Tiempo
    t_points = [k*x for x in t]
    print "t_points", t_points
    #print "Tiempo de recorrido",t_rec,"s" 
    [j,ext]=generate_path_cub(q,t_points,F)
    [v,ext]=generate_vel(j,F)
    [a,ext]=generate_acel(v,F)
    [jk,v_jk,ext]=generate_jerk(a,F)
    v_t=6*(t_points[-1]-t_points[0])
    raw_input('Iniciar?')
    print "Valor tiempo: ",v_t,"Valor jerk", v_jk
    save_matrix(j,"save_data_p.txt",F)
    save_matrix(v,"save_data_v.txt",F)
    save_matrix(a,"save_data_a.txt",F)
    save_matrix(jk,"save_data_y.txt",F)
    
    ik_service_client_full(0.662,0.450,-0.040,0.717,0,0.717,0)
    time.sleep(1)
    my_msg=JointCommand()
    my_msg.mode=4
    my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]
    
    real_data=Getdata("S_data.txt")
    real_data.writeon()
    time.sleep(0.75)
    if(my_msg.mode==1):
        for n in range(ext): 
            my_msg.position=[j[0][n],j[1][n],j[2][n],j[3][n],j[4][n],j[5][n],j[6][n]]
            pub.publish(my_msg)
            rate.sleep()
    if(my_msg.mode==2):
        for n in range(ext): 
            my_msg.velocity=[v[0][n],v[1][n],v[2][n],v[3][n],v[4][n],v[5][n],v[6][n]]
            pub.publish(my_msg)
            rate.sleep()
    if(my_msg.mode==4):
        for n in range(ext): 
            my_msg.position=[j[0][n],j[1][n],j[2][n],j[3][n],j[4][n],j[5][n],j[6][n]]
            my_msg.velocity=[v[0][n],v[1][n],v[2][n],v[3][n],v[4][n],v[5][n],v[6][n]]
            my_msg.acceleration=[a[0][n],a[1][n],a[2][n],a[3][n],a[4][n],a[5][n],a[6][n]]   
            pub.publish(my_msg)
            rate.sleep()
    time.sleep(0.75)
    return True

def main():

    print("Initializing node... ")
    rospy.init_node("sdk_joint_trajectory")
    print("Getting robot state... ")
    rs = intera_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled
    rate = rospy.Rate(100) # hz
    rospy.loginfo("Enabling robot...")
    rs.enable()
    set_move()
    time.sleep(0.5)   
    print("Done.")


if __name__ == '__main__':
    main()










