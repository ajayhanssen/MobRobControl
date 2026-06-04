# Stolen from
# https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Broadcaster-Py.html
# with slight modifications

#-------------------------------------------------------------------------------#
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster

from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import PoseWithCovarianceStamped
#-------------------------------------------------------------------------------#


class FramePublisher(Node):

    def __init__(self):
        super().__init__('mobrob_tf2_frame_publisher')

        # Declare and acquire `robname` parameter
        self.robname = self.declare_parameter('robname', 'rob1').get_parameter_value().string_value

        # Initialize the transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # Subscribe to a rob{1}{2}/pose topic and call handle_rob_pose
        # callback function on each message
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            f'/{self.robname}/pose',
            self.handle_rob_pose,
            1)
        self.subscription  # prevent unused variable warning

    def handle_rob_pose(self, msg):
        t = TransformStamped()

        # Read message content and assign it to
        # corresponding tf variables
        t.header.stamp = msg.header.stamp
        t.header.frame_id = 'map'
        t.child_frame_id = self.robname

        t.transform.translation.x = msg.pose.pose.position.x
        t.transform.translation.y = msg.pose.pose.position.y
        t.transform.translation.z = msg.pose.pose.position.z

        t.transform.rotation.x = msg.pose.pose.orientation.x
        t.transform.rotation.y = msg.pose.pose.orientation.y
        t.transform.rotation.z = msg.pose.pose.orientation.z
        t.transform.rotation.w = msg.pose.pose.orientation.w

        self.tf_broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = FramePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()