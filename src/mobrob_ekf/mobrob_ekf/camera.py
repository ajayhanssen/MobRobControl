#-------------------------------------------------------------------------------#
import rclpy
import math
import random
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
#-------------------------------------------------------------------------------#


class Camera(Node):
    def __init__(self):
        super().__init__('robot_simulation_node')
        
        self.odom_pub = self.create_publisher(Odometry, '/rob1/odom', 10)
        self.pose_pub = self.create_publisher(PoseWithCovarianceStamped, '/rob1/pose', 10)
        
        # Ground truth state trackers
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        
        self.linear_v = 0.4   
        self.angular_v = 0.2  
        
        self.last_time = self.get_clock().now()
        
        self.create_timer(1.0 / 20.0, self.publish_odom)  # 20 Hz
        self.create_timer(1.0 / 2.0, self.publish_pose)    # 2 Hz

    def update_ground_truth(self, current_time):
        dt = (current_time - self.last_time).nanoseconds / 1e9
        if dt > 0:
            self.yaw += self.angular_v * dt
            self.x += self.linear_v * math.cos(self.yaw) * dt
            self.y += self.linear_v * math.sin(self.yaw) * dt
            self.last_time = current_time

    def publish_odom(self):
        now = self.get_clock().now()
        self.update_ground_truth(now)
        
        odom = Odometry()
        odom.header.stamp = now.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        
        odom.twist.twist.linear.x = self.linear_v + random.gauss(0, 0.01)
        odom.twist.twist.angular.z = self.angular_v + random.gauss(0, 0.005)
        
        odom.twist.covariance[0] = 0.01   
        odom.twist.covariance[35] = 0.005  
        
        self.odom_pub.publish(odom)

    def publish_pose(self):
        now = self.get_clock().now()
        self.update_ground_truth(now)
        
        pose_msg = PoseWithCovarianceStamped()
        pose_msg.header.stamp = now.to_msg()
        pose_msg.header.frame_id = 'map'  # cam sees rob in global frame
        
        pose_msg.pose.pose.position.x = self.x + random.gauss(0, 0.005)
        pose_msg.pose.pose.position.y = self.y + random.gauss(0, 0.005)
        
        pose_msg.pose.pose.orientation.z = math.sin(self.yaw / 2.0)
        pose_msg.pose.pose.orientation.w = math.cos(self.yaw / 2.0)
        
        # Give the camera a realistic, slightly larger covariance matrix
        pose_msg.pose.covariance[0] = 0.01   # x variance
        pose_msg.pose.covariance[7] = 0.01   # y variance
        pose_msg.pose.covariance[35] = 0.05  # yaw variance
        
        self.pose_pub.publish(pose_msg)

def main(args=None):
    rclpy.init(args=args)
    node = Camera()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()