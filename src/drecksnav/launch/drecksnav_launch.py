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

    rviz_config = os.path.join(pkg_share, 'rviz', 'ekf_v3.rviz')
    ekf_config_path = os.path.join(pkg_share, 'config', 'ekf.yaml')
    twist_mux_config_path = os.path.join(pkg_share, 'config', 'twist_mux.yaml')

    nav2_config_path = os.path.join(pkg_share, 'config', 'nav2_params.yaml')
    map_yaml_path = os.path.join(pkg_share, 'maps', 'map.yaml')

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
            remappings=[('/odometry/filtered', '/odometry/local')] # remap to unique output topic
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node_map',
            output='screen',
            parameters=[ekf_config_path, use_sim_time],
            remappings=[('/odometry/filtered', '/odometry/global')] # remap to anotha output topic
        ),

        # camera
        Node(
            package='drecksnav',
            executable='camera',
            name='cam',
            parameters=[
                {'robname': 'rob1'},
                use_sim_time,
            ]
        ),
        
        # nav2
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[nav2_config_path, 
                        {'yaml_filename': map_yaml_path}, 
                        {'use_sim_time': use_sim_time}]
        ),
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[nav2_config_path, {'use_sim_time': use_sim_time}]
        ),
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[nav2_config_path, {'use_sim_time': use_sim_time}],
            # Remap output velocity if using twist_mux
            remappings=[('/cmd_vel', '/rob1/cmd_vel')] 
        ),
        Node(
            package='nav2_behaviors',
            executable='behavior_server',
            name='behavior_server',
            output='screen',
            parameters=[nav2_config_path, {'use_sim_time': use_sim_time}]
        ),
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[nav2_config_path, {'use_sim_time': use_sim_time}]
        ),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'autostart': True,
                'node_names': [
                    'map_server', 
                    'planner_server', 
                    'controller_server', 
                    'behavior_server', 
                    'bt_navigator'
                ]
            }]
        ),
    ])