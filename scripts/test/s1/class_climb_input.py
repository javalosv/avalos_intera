import rospy
import argparse
from intera_interface import Limb

def main():

    try:
        rospy.init_node('avalos_limb_py')
        limb = Limb()

        print "Joint Name:"
        print limb.joint_names()

        print "\n"+"Joint Angles:"
        print limb.joint_angles()

        print "\n"+"Joint Velocities:"
        print limb.joint_velocities()

        print "\n"+"Endpoint Pose:"
        print limb.endpoint_pose()

        print "\n"+"Endpoint Velocity:"
        print limb.endpoint_velocity()

    except rospy.ROSInterruptException:
        rospy.logerr('Keyboard interrupt detected from the user. Exiting before trajectory completion.')



if __name__ == '__main__':
    main()
