#-------------------------------------------------------------------------------#
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist
#-------------------------------------------------------------------------------#

class RobotSafetyWatchdog(Node):
    def __init__(self):
        super().__init__('robot_safety_watchdog')

        self.robname = self.declare_parameter('robname', 'rob1').get_parameter_value().string_value

        # lat time cam was there
        self.last_camera_time = self.get_clock().now()
        self.camera_lost = False

        # sub to camera pose
        self.create_subscription(
            PoseWithCovarianceStamped, 
            f'/{self.robname}/pose', 
            self.camera_callback, 
            10
        )
        
        # pub for sending to emergency vel topic
        self.cmd_vel_pub = self.create_publisher(Twist, f'/{self.robname}/cmd_vel_emergency', 10)

        # Check safety status at 10 Hz
        self.create_timer(1/10, self.safety_check_callback)

    def camera_callback(self, msg):
        self.last_camera_time = self.get_clock().now()
        if self.camera_lost:
            self.get_logger().info("Camera is BACK!.")
            self.camera_lost = False

    def safety_check_callback(self):
        # calc time since last camera message
        elapsed_time = (self.get_clock().now() - self.last_camera_time).nanoseconds / 1e9

        if elapsed_time > 1.0: # 1 second limit
            if not self.camera_lost:
                self.get_logger().error("Camera signal lost for > 1.0s, robot stops now.")
                self.camera_lost = True
            
            # force sotp
            stop_msg = Twist()
            stop_msg.linear.x = 0.0
            stop_msg.angular.z = 0.0
            self.cmd_vel_pub.publish(stop_msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotSafetyWatchdog()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()