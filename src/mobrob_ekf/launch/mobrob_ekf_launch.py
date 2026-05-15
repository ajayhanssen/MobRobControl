#-------------------------------------------------------------------------------#
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition

from ament_index_python.packages import get_package_share_directory
import os
#-------------------------------------------------------------------------------#


def generate_launch_description():

    pkg_share = get_package_share_directory('mobrob_ekf')

    rviz_config = os.path.join(pkg_share, 'rviz', 'ekf2.rviz')

    ekf_config_path = os.path.join(pkg_share, 'config', 'ekf.yaml')

    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz',
        default_value='true',
        description='true -> Rviz, false -> pygame'
    )

    use_rviz = LaunchConfiguration('use_rviz')

    return LaunchDescription([

        use_rviz_arg,

        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_local',
            output='screen',
            parameters=[ekf_config_path],
            remappings=[('/odometry/filtered', '/odometry/local')]
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_global',
            output='screen',
            parameters=[ekf_config_path],
            remappings=[('/odometry/filtered', '/odometry/global')]
        ),

        # rob controller
        Node(
            package='mobrob_ekf',
            executable='controller',
            name='controller1',
            parameters=[
                {'robname': 'rob1',
                 'lin_vel': 0.2,
                 'max_angular_vel': 1.51,
                 'lookahead_dist': 0.1}
            ]
        ),

        # camera
        Node(
            package='mobrob_ekf',
            executable='camera',
            name='cam',
            parameters=[
                {'robname': 'rob1'}
            ]
        ),
        # path
        Node(
            package='mobrob_ekf',
            executable='path_publisher',
            name='path_pub',
            parameters=[
                {'robname': 'rob1'}
            ]
        ),

        # Rviz
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            condition=IfCondition(use_rviz),
            output='screen'
        ),

        # or pygame
        Node(
            package='mobrob_ekf',
            executable='visualizer',
            name='tv_visualizer',
            condition=UnlessCondition(use_rviz),
            parameters=[
                {'robname': 'rob1'}
            ]
        ),
    ])