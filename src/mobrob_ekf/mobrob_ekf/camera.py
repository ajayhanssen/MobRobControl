#-------------------------------------------------------------------------------#
import rclpy
import math
import random
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
#-------------------------------------------------------------------------------#


class CameraSimNode(Node):
    def __init__(self):
        super().__init__('camera_sim_node')

        self._latest_odom: Odometry | None = None

        #self.declare_parameter('use_sim_time', True)

        self.create_subscription(Odometry, '/rob1/odom', self._odom_callback, 10)
        self.pose_pub = self.create_publisher(PoseWithCovarianceStamped, '/rob1/pose', 10)

        self.create_timer(1.0 / 2.0, self._publish_pose)  # 2 Hz

    def _odom_callback(self, msg: Odometry):
        self._latest_odom = msg

    def _publish_pose(self):
        if self._latest_odom is None:
            return

        src_pose = self._latest_odom.pose.pose

        pose_msg = PoseWithCovarianceStamped()
        pose_msg.header.stamp = self._latest_odom.header.stamp
        pose_msg.header.frame_id = 'map'

        pose_msg.pose.pose.position.x = src_pose.position.x + random.gauss(0, 0.005)
        pose_msg.pose.pose.position.y = src_pose.position.y + random.gauss(0, 0.005)
        pose_msg.pose.pose.position.z = src_pose.position.z
        pose_msg.pose.pose.orientation = src_pose.orientation

        pose_msg.pose.covariance[0]  = 0.01   # x variance
        pose_msg.pose.covariance[7]  = 0.01   # y variance
        pose_msg.pose.covariance[35] = 0.05   # yaw variance

        self.pose_pub.publish(pose_msg)


def main(args=None):
    rclpy.init(args=args)
    node = CameraSimNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()