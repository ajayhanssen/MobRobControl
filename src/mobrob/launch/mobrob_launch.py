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

    pkg_share = get_package_share_directory('mobrob')
    rviz_config = os.path.join(pkg_share, 'rviz', 'mobrob.rviz')
    twist_mux_config_path = os.path.join(pkg_share, 'config', 'twist_mux.yaml')

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (clock topic) clock if true'
    )

    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz',
        default_value='true',
        description='true -> Rviz, false -> pygame'
    )

    use_sim_time = {'use_sim_time': LaunchConfiguration('use_sim_time')}
    use_rviz = LaunchConfiguration('use_rviz')

    return LaunchDescription([
        use_sim_time_arg,
        use_rviz_arg,

        # tf2 broadcaster
        Node(
            package='mobrob',
            executable='tf2_broadcaster',
            name='tf2_broadcaster1',
            parameters=[
                {'robname': 'rob1'},
                use_sim_time,
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
                 'lookahead_dist': 0.3},
                 use_sim_time
            ]
        ),

        # camera
        Node(
            package='mobrob',
            executable='camera',
            name='cam',
            parameters=[
                {'robname': 'rob1'},
                use_sim_time
            ]
        ),
        # path
        Node(
            package='mobrob',
            executable='path_publisher',
            name='path_pub',
            parameters=[
                {'robname': 'rob1'},
                use_sim_time
            ]
        ),

        Node(
            package='twist_mux',
            executable='twist_mux',
            name='twist_mux',
            output='screen',
            parameters=[twist_mux_config_path],
            remappings=[('/cmd_vel_out', '/rob1/cmd_vel')]
        ),

        # watchdog
        Node(
            package='mobrob',
            executable='watchdog',
            name='watchdog_cam',
            parameters=[
                {'robname': 'rob1'},
                use_sim_time,
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
                {'robname': 'rob1'},
                use_sim_time
            ]
        ),
    ])