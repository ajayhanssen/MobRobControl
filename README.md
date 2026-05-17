# MobRobControl

ROS2 Humble package for Project 1; MA-MECH-25-VZ.  

Source dependencies:
~~~
source install/setup.bash
~~~

Launch nodes:
~~~
ros2 launch mobrob_ekf mobrob_ekf_launch.py
~~~

REP105:
map -> odom -> base_link

ros2 launch gazebo_ros gazebo.launch.py

sudo apt update
sudo apt install ros-humble-robot-localization
sudo apt install ros-humble-gazebo-ros-pkgs