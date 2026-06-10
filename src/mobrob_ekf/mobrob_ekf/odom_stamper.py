#-------------------------------------------------------------------------------#
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
#-------------------------------------------------------------------------------#

class OdometryStamper(Node):
    def __init__(self):
        super().__init__('odometry_stamper')

        self.robname = self.declare_parameter('robname', 'rob1').get_parameter_value().string_value

        self.create_subscription(Odometry, f'/{self.robname}/odom', self._odom_callback, 10)
        self.odom_pub = self.create_publisher(Odometry, f'/{self.robname}/odom_stamped', 10)

    def _odom_callback(self, msg: Odometry):
        msg.header.stamp = self.get_clock().now().to_msg()
        #msg.header.stamp.sec = 0       # kein timestamp gnagget alles
        #msg.header.stamp.nanosec = 0
        msg.pose.pose.position.x = 0.0
        msg.pose.pose.position.y = 0.0
        msg.pose.pose.position.z = 0.0
        msg.pose.pose.orientation.x = 1.0
        msg.pose.pose.orientation.y = 0.0
        msg.pose.pose.orientation.z = 0.0
        msg.pose.pose.orientation.w = 0.0

        self.odom_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = OdometryStamper()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()