#-------------------------------------------------------------------------------#
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
#-------------------------------------------------------------------------------#


class Camera(Node):
    def __init__(self):
        super().__init__('camera')

        self.robname = self.declare_parameter('robname', 'rob1').get_parameter_value().string_value

        self.publisher_ = self.create_publisher(PoseStamped, f'/{self.robname}/pose', 1)

        timer_period = 0.1 # secondas
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = PoseStamped()
        msg.header.frame_id = 'world'
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = 0.2
        msg.pose.position.y = 0.1
        msg.pose.position.z = 0.0

        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.0
        msg.pose.orientation.w = 1.0

        self.publisher_.publish(msg)
        self.get_logger().info(f"Sent: {msg} .")


def main(args=None):
    rclpy.init(args=args)

    minimal_publinger = Camera()

    rclpy.spin(minimal_publinger)


    minimal_publinger.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()