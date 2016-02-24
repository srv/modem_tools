cmake_minimum_required(VERSION 2.8.3)
project(modem_tools)

find_package(catkin REQUIRED COMPONENTS
            rospy
            auv_msgs
            diagnostic_msgs)

catkin_package()

catkin_python_setup()
