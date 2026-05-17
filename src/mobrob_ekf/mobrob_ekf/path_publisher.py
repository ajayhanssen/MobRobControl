#-------------------------------------------------------------------------------#
import rclpy
from rclpy.node import Node

from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

import numpy as np
#-------------------------------------------------------------------------------#


class PathPublisher(Node):
    def __init__(self):
        super().__init__('path_planner')

        self.robname = self.declare_parameter('robname', 'rob1').get_parameter_value().string_value

        self.publisher = self.create_publisher(Path, f'{self.robname}/path', 1)
        timer_period = 5.0 # secondas
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Path()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()

        #self.publisher.publish(msg)
        #self.get_logger().info(f"Sent: {msg} .")

        # test circle
        radius = 1.0 #m
        num_points = 50

        for i in range(num_points):
            angle = 2 * np.pi * i / num_points
            
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.pose.position.x = 3 + radius * np.cos(angle)
            pose.pose.position.y = 3 + radius * np.sin(angle)
            pose.pose.position.z = 0.0
            
            msg.poses.append(pose)

        self.publisher.publish(msg)
        #self.get_logger().info(f"Published circle path with {num_points} points")


def main(args=None):
    rclpy.init(args=args)

    path_pub = PathPublisher()

    rclpy.spin(path_pub)


    path_pub.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()