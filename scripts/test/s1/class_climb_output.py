import rospy
import argparse
from intera_interface import Limb

def main():

    try:
        rospy.init_node('avalos_limb_py')
        rate = rospy.Rate(100)
        limb = Limb()
        positions={"right_j6": 0.0,
                    "right_j5": 0.0,
                    "right_j4": 0.0,
                    "right_j3": 0.0,
                    "right_j2": 0.0,
                    "right_j1": 0.0,
                    "right_j0": 0.0}
        print positions
        limb.move_to_joint_positions(positions)
        print "Moveo ok"

    except rospy.ROSInterruptException:
        rospy.logerr('Keyboard interrupt detected from the user. Exiting before trajectory completion.')



if __name__ == '__main__':
    main()
