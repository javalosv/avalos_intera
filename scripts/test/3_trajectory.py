import argparse
import rospy
import intera_interface
import intera_external_devices
from intera_interface import CHECK_VERSION
from intera_core_msgs.msg import JointCommand
import time
import record_data #file to record data.

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

import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import UnivariateSpline
from scipy.interpolate import interp1d
import numpy as np
import os


def set_j():
    
    limb = intera_interface.Limb('right')
    limb.move_to_neutral()
    print "Posicion neutral terminada"
    #time.sleep(1)
    ik_service_client(0.680,0.300,0.040)
    print "Posicion inicial terminada"
    names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]
    
    
    

    k=2.5  #Factor de Tiempo
    F=100   #Frecuencia de envio
    rate = rospy.Rate(F) # hz
    pub = rospy.Publisher('/robot/limb/right/joint_command', JointCommand, queue_size=10)
    my_msg=JointCommand()
    my_msg.mode=1
    my_msg.names=["right_j0","right_j1","right_j2","right_j3","right_j4","right_j5","right_j6"]

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

    sp_0 = interpolate.UnivariateSpline(t_points, j_points[0][:],k=5)
    sp_1 = interpolate.UnivariateSpline(t_points, j_points[1][:],k=5)
    sp_2 = interpolate.UnivariateSpline(t_points, j_points[2][:],k=5)
    sp_3 = interpolate.UnivariateSpline(t_points, j_points[3][:],k=5)
    sp_4 = interpolate.UnivariateSpline(t_points, j_points[4][:],k=5)
    sp_5 = interpolate.UnivariateSpline(t_points, j_points[5][:],k=5)
    sp_6 = interpolate.UnivariateSpline(t_points, j_points[6][:],k=5)


    ts = np.linspace(t_points[0], t_points[-1], (t_points[-1]-t_points[0])*F)  # de 
    
    j0= sp_0(ts)
    j1= sp_1(ts)
    j2= sp_2(ts)
    j3= sp_3(ts)
    j4= sp_4(ts)
    j5= sp_5(ts)
    j6= sp_6(ts)

    print len(ts)

    file2write=open("data_send_6_58_07_07.txt",'w')
    
    for n in range(len(j0)): 
        file2write.write(str(j0[n])+' , '+str(j1[n])+' , '+str(j2[n])+' , '+str(j3[n])+' , '+ \
        str(j4[n])+' , '+str(j5[n])+' , '+str(j6[n])+'\n')
    file2write.close()

    raw_input('Iniciar?')

    for n in range(len(j0)):    
        my_msg.position=[j0[n],j1[n],j2[n],j3[n],j4[n],j5[n],j6[n]]
        pub.publish(my_msg)
        #limb.move_to_joint_positions(joint_command)
        rate.sleep()
    print my_msg.position 



    return True


def ik_service_client(_x,_y,_z):
    _limb = intera_interface.Limb('right')
    ns = "ExternalTools/right/PositionKinematicsNode/IKService"
    iksvc = rospy.ServiceProxy(ns, SolvePositionIK)
    ikreq = SolvePositionIKRequest()
    hdr = Header(stamp=rospy.Time.now(), frame_id='base')
    poses = {
        'right': PoseStamped(
            header=hdr,
            pose=Pose(
                position=Point(
                    x=_x,
                    y=_y,
                    z=_z,
                ),
                orientation=Quaternion(
                    x=0.707,
                    y=0.707,
                    z=0.001,
                    w=0.001,
                ),
            ),
        ),
    }
    # Add desired pose for inverse kinematics
    ikreq.pose_stamp.append(poses["right"])
    # Request inverse kinematics from base to "right_hand" link
    ikreq.tip_names.append('right_hand')


    try:
        rospy.wait_for_service(ns, 5.0)
        resp = iksvc(ikreq)
    except (rospy.ServiceException, rospy.ROSException), e:
        rospy.logerr("Service call failed: %s" % (e,))
        return False

    # Check if result valid, and type of seed ultimately used to get solution
    if (resp.result_type[0] > 0):
        # Format solution into Limb API-compatible dictionary
        limb_joints = dict(zip(resp.joints[0].name, resp.joints[0].position))
        rospy.loginfo("Solucion IK ok:\n")
        print limb_joints
        _limb.move_to_joint_positions(limb_joints)
        return True
    else:
        rospy.logerr("INVALID POSE - No Valid Joint Solution Found.")
        rospy.logerr("Result Error %d", resp.result_type[0])
        return False

    
def main():

    print("Initializing node... ")
    rospy.init_node("sdk_joint_trajectory")
    print("Getting robot state... ")
    rs = intera_interface.RobotEnable(CHECK_VERSION)
    print rs.version_check()
    init_state = rs.state().enabled
    rate = rospy.Rate(100) # hz

    rospy.loginfo("Enabling robot...")
    rs.enable()

    set_j()
    
    print("Done.")


if __name__ == '__main__':
    main()
