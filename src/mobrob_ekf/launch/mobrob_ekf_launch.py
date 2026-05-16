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

        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_odom',
            output='screen',
            parameters=[ekf_config_path, use_sim_time],
            remappings=[('/odometry/filtered', '/odometry/local')] # Unique output topic
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_map',
            output='screen',
            parameters=[ekf_config_path, use_sim_time],
            remappings=[('/odometry/filtered', '/odometry/global')] # Unique output topic
        ),

        Node(
            package='mobrob_ekf',
            executable='controller',
            name='controller1',
            parameters=[
                {'robname': 'rob1',
                 'lin_vel': 0.2,
                 'max_angular_vel': 1.51,
                 'lookahead_dist': 0.3,
                 },
                 use_sim_time,
            ]
        ),


        # camera
        Node(
            package='mobrob_ekf',
            executable='camera',
            name='cam',
            parameters=[
                {'robname': 'rob1'},
                use_sim_time,
            ]
        ),

        # path
        Node(
            package='mobrob_ekf',
            executable='path_publisher',
            name='path_pub',
            parameters=[
                {'robname': 'rob1'},
                use_sim_time
            ]
        ),

        # Rviz
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            condition=IfCondition(use_rviz),
            parameters=[use_sim_time],
            output='screen'
        ),

        # or pygame
        Node(
            package='mobrob_ekf',
            executable='visualizer',
            name='tv_visualizer',
            condition=UnlessCondition(use_rviz),
            parameters=[
                {'robname': 'rob1'},
                use_sim_time,
            ]
        ),
    ])