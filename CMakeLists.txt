cmake_minimum_required(VERSION 2.8.3)
project(avalos_intera)

find_package(catkin
  REQUIRED
  COMPONENTS
  cv_bridge
  rospy
  actionlib
  sensor_msgs
  std_msgs
  control_msgs
  trajectory_msgs
  dynamic_reconfigure
  intera_core_msgs
  intera_motion_msgs
  message_generation
)

catkin_python_setup()

generate_dynamic_reconfigure_options(
  cfg/SawyerPositionJointTrajectoryActionServer.cfg
  cfg/SawyerVelocityJointTrajectoryActionServer.cfg
  cfg/SawyerPositionFFJointTrajectoryActionServer.cfg
)

add_dependencies(${PROJECT_NAME}_gencfg intera_core_msgs_generate_messages_py)


add_message_files(
  FILES
  robot_q.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime
  cv_bridge
  rospy
  actionlib
  sensor_msgs
  std_msgs
  control_msgs
  trajectory_msgs
  dynamic_reconfigure
  intera_core_msgs
  intera_motion_msgs
)

install(
  DIRECTORY scripts/ scripts/test/ utec-iot/ 
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  USE_SOURCE_PERMISSIONS
)

