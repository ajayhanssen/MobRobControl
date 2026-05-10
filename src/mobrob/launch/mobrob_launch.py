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

    rviz_config = os.path.join(
        get_package_share_directory('mobrob'),
        'rviz',
        'mobrob.rviz'
    )

    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz',
        default_value='true',
        description='true -> Rviz, false -> pygame'
    )

    use_rviz = LaunchConfiguration('use_rviz')

    return LaunchDescription([

        use_rviz_arg,

        # tf2 broadcaster
        Node(
            package='mobrob',
            executable='tf2_broadcaster',
            name='tf2_broadcaster1',
            parameters=[
                {'robname': 'rob1'}
            ]
        ),

        # rob controller
        Node(
            package='mobrob',
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
            package='mobrob',
            executable='camera',
            name='cam',
            parameters=[
                {'robname': 'rob1'}
            ]
        ),
        # path
        Node(
            package='mobrob',
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
            package='mobrob',
            executable='visualizer',
            name='tv_visualizer',
            condition=UnlessCondition(use_rviz),
            parameters=[
                {'robname': 'rob1'}
            ]
        ),
    ])