avalos_intera
================

2018

Python interface classes and action servers for control of
the Intera Research Robot from Rethink Robotics

Code & Tickets
--------------

+-----------------+----------------------------------------------------------------+
| Documentation   | http://sdk.rethinkrobotics.com/intera/                         |
+-----------------+----------------------------------------------------------------+
| Issues          | https://github.com/RethinkRobotics/avalos_intera/issues     |
+-----------------+----------------------------------------------------------------+
| Contributions   | http://sdk.rethinkrobotics.com/intera/Contributions            |
+-----------------+----------------------------------------------------------------+



avalos_intera Repository Overview
------------------------------------
     jose@avalos:~/avalos_ros_ws/src$ tree -L 2
::
     .
     |
     +-- CMakeLists.txt -> /opt/ros/kinetic/share/catkin/cmake/toplevel.cmake
     |
     +--intera_common
     |   +--  CHANGELOG.rst
     |   +--  CONTRIBUTING.md
     |   +--  intera_common
     |   +--  intera_core_msgs
     |   +--  intera_motion_msgs
     |   +--  intera_tools_description
     |   +--  LICENSE
     |   +--  README.rst
     +--intera_sdk
     |   +--  avalos_intera <<<--------------------------------------------------------
     |   +--  CHANGELOG.rst
     |   +--  CONTRIBUTING.md
     |   +--  intera_examples
     |   +--  intera_interface
     |   +--  intera_sdk
     |   +--  intera.sh
     |   +--  LICENSE
     |   +--  README.rst
     +--sawyer_robot
     |   +--  CHANGELOG.rst
     |   +--  CONTRIBUTING.md
     |   +--  LICENSE
     |   +--  README.rst
     |   +--  sawyer_description
     |   +--  sawyer_robot
     |   +--  sawyer_robot.rosinstall
     +--sawyer_simulator
     |   +--  CONTRIBUTING.md
     |   +--  LICENSE
     |   +--  README.rst
     |   +--  sawyer_gazebo
     |   +--  sawyer_hardware_interface
     |   +--  sawyer_sim_controllers
     |   +--  sawyer_sim_examples
     |   +--  sawyer_simulator
     |   +--  sawyer_simulator.rosinstall

19 directories, 19 files


::

     .
     |
     +-- src/                                  avalos_intera api
     |   +-- intera_io/                        basic interface for IO Framework
     |   +-- intera_interface/                 intera component classes
     |       +-- camera.py
     |       +-- cuff.py
     |       +-- digital_io.py
     |       +-- gripper.py
     |       +-- head.py
     |       +-- head_display.py
     |       +-- lights.py
     |       +-- limb.py
     |       +-- navigator.py
     |       +-- robot_enable.py
     |       +-- robot_params.py
     |       +-- settings.py
     |   +-- intera_control/                   generic control utilities
     |   +-- intera_dataflow/                  timing/program flow utilities
     |   +-- intera_joint_trajectory_action/   joint trajectory action implementation
     |
     +-- scripts/                              utility executable scripts
     |   +-- calibrate_arm.py                  arm calibration action client
     |   +-- enable_robot.py                   enable / disable / reset the robot
     |   +-- home_joints.py                    script to home the joints on the robot
     |   +-- joint_trajectory_action_server.py trajectory action server for use with MoveIt
     |   +-- send_urdf_fragment.py             send URDF fragment to update robot's URDF
     |
     +-- cfg/                                  dynamic reconfigure action configs


Other Intera Repositories
-------------------------

+------------------+-----------------------------------------------------+
| intera_common    | https://github.com/RethinkRobotics/intera_common    |
+------------------+-----------------------------------------------------+

Latest Release Information
--------------------------

http://sdk.rethinkrobotics.com/intera/Release-Changes
