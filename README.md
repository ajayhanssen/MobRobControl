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

~~~
sudo apt update
sudo apt install ros-humble-robot-localization
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install ros-humble-twist-mux
~~~

## Start gazebo
~~~
ros2 launch gazebo_ros gazebo.launch.py
~~~
Then insert the robot model into the world.

## Useful cmds:
### Set velocity to 0
~~~
ros2 topic pub /rob1/cmd_vel geometry_msgs/msg/Twist '{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'
ros2 topic pub /rob1/cmd_vel_emergency geometry_msgs/msg/Twist '{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'
~~~

### Teleop key
~~~
ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=/rob1/cmd_vel_teleop --param scale_linear:=0.1 --param scale_angular:=0.1
~~~

### Disable cam publishing for emergency stop
~~~
ros2 param set /cam enable_publishing false
~~~