import argparse
import rospy
import intera_interface
import intera_external_devices
import time
import record_data #file to record data.
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


def set_j():
    
    limb = intera_interface.Limb('right')
    limb.move_to_neutral()
    print "Posicion neutral terminada"
    #time.sleep(1)
    ik_service_client(0.680,0.300,0.040)
    print "Posicion inicial terminada"
    names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]

    k=3  #Factor de Tiempo
    F=100   #Frecuencia de envio
    rate = rospy.Rate(F) # hz
    pub = rospy.Publisher('/robot/limb/right/joint_command', JointCommand, queue_size=10)
   
    t=[0, 1, 2, 3, 4, 5, 6];
    t_points = [k*x for x in t]
    # Inicia en el joint 0-6
    j_points=[[-0.0497081518 ,   -0.0537617656 ,  -0.245754079 ,   -0.1561610521,   -0.4432674925 ,  -0.5804805548,   -0.9952186238] ,\
    [-0.4451660593,  -0.634860939,    -0.6609938085 ,  -0.8471579158  , -0.8995330045 ,  -0.6558273922 ,  -0.434025672] ,\
    [0.4873428837 ,  0.1991682519 ,   0.2152131246  ,  0.0130412921 ,   0.2191921688  ,  0.171808715, 0.7121382962] ,\
    [1.2309618386 ,  1.7489810486 ,   1.8203601335,    1.502603275 ,1.539734643 ,1.8250517027 ,   1.2631597975] ,\
    [-0.5633900383,  -0.3468272648 ,  -0.3965199381 ,  0.0115052335,    -0.1665613231  , -0.330217831 ,   -0.7716105727] ,\
    [0.91  , 0.488365349, 0.450784998 ,0.9126277329 ,   0.9462226755,    0.4267531801  ,  1.012701208] ,\
    [-2.4257682103 , -2.5931771058,   -2.719486461 ,   -3.14 ,  -3.14 ,  -3.14,   -3.14]]
    # J devuelto como lista 
    [j,ext]=generate_path(j_points,t_points,F)
    [v,ext]=generate_vel(j,F)
    [a,ext]=generate_acel(v,F)
    [jk,ext]=generate_jerk(a,F)
    save_matrix(j,"save_data_p.txt",F)
    save_matrix(v,"save_data_v.txt",F)
    save_matrix(a,"save_data_a.txt",F)
    save_matrix(jk,"save_data_y.txt",F)

    raw_input('Iniciar?')

    my_msg=JointCommand()
    my_msg.mode=4
    my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]
    real_data=Rdata("save_real_data.txt")
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
    set_j()   
    print("Done.")


if __name__ == '__main__':
    main()
