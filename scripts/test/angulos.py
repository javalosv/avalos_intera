import argparse
import rospy
import intera_interface
import intera_external_devices
from intera_interface import CHECK_VERSION
import time

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
    print "Posicion neutral finalizada \n"
    #joint_command={"right_j6": 0.0, "right_j5": 0.0, "right_j4": 0.0, "right_j3": 0.0, "right_j2": 0.0, "right_j1": 0.0, "right_j0": 0.0}  
    ik_service_client(0.680,0.300,0.040)
    ik_service_client(0.550,0.200,0.040)
    ik_service_client(0.550,0.100,0.040)
    ik_service_client(0.680,0.050,0.240)
    ik_service_client(0.680,-0.050,0.240)
    ik_service_client(0.550,-0.100,0.040)
    ik_service_client(0.680,-0.300,0.040)


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
    rospy.init_node("sdk_joint_position_keyboard")
    print("Getting robot state... ")
    rs = intera_interface.RobotEnable(CHECK_VERSION)
    print rs.version_check()
    init_state = rs.state().enabled

    rospy.loginfo("Enabling robot...")
    rs.enable()

    set_j()
    
    print("Done.")


if __name__ == '__main__':
    main()
