# huge inspiration for the tf2 listener part from
# https://docs.ros.org/en/humble/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Listener-Py.html

#-------------------------------------------------------------------------------#
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Path

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

import numpy as np
#-------------------------------------------------------------------------------#


class MobrobController(Node):

    def __init__(self):
        super().__init__('mobrob_controller')

        # launch parameters (also pure pursuit)
        self.robname = self.declare_parameter('robname', 'rob1').get_parameter_value().string_value
        self.linear_velocity = self.declare_parameter('lin_vel', 0.11).get_parameter_value().double_value
        self.max_angular_vel = self.declare_parameter('max_angular_vel', np.pi/2).get_parameter_value().double_value
        self.lookahead_distance = self.declare_parameter('lookahead_dist', 0.1).get_parameter_value().double_value
        
        self.path = None
        
        # tf2 listener setup
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # path subscriber
        self.path_sub = self.create_subscription(Path, f'/{self.robname}/path', self.path_callback, 10)

        # velocity publisher
        self.ctrl_cmd_pub = self.create_publisher(Twist, f'/{self.robname}/cmd_vel', 10)

        # create 10Hz control loop
        self.timer = self.create_timer(0.1, self.control_loop)


    def path_callback(self, msg):
        #self.get_logger().info(f"Received path with {len(msg.poses)} waypoints")
        self.path = msg


    def control_loop(self):

        if self.path is None or len(self.path.poses) == 0:
            self.get_logger().info('No path loaded!')
            return
        
        try:
            # get most recent transform
            now = rclpy.time.Time()
            trans = self.tf_buffer.lookup_transform('world', self.robname, now)

            # get translation
            robot_x = trans.transform.translation.x
            robot_y = trans.transform.translation.y

            target_point = self.get_lookahead_point(robot_x, robot_y)

            if target_point:
                # to local coord frame
                dx = target_point.x - robot_x
                dy = target_point.y - robot_y

                # calc orientation
                q = trans.transform.rotation
                siny_cosp = 2 * (q.w * q.z + q.x * q.y)
                cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
                yaw = np.arctan2(siny_cosp, cosy_cosp)

                local_x = dx * np.cos(-yaw) - dy * np.sin(-yaw)
                local_y = dx * np.sin(-yaw) + dy * np.cos(-yaw)

                # pure pursuitinger
                curvature = (2.0*local_y) / self.lookahead_distance**2
                msg = Twist()
                msg.linear.x = self.linear_velocity
                msg.angular.z = np.clip(self.linear_velocity * curvature, -self.max_angular_vel, self.max_angular_vel)

                self.ctrl_cmd_pub.publish(msg)


        except TransformException as ex:
            self.get_logger().info(
                f'Could not transform world to {self.robname}: {ex}')
            return
    
    def get_lookahead_point(self, rx, ry):
        num_poses = len(self.path.poses)
        if num_poses == 0:
            return None
        
        distances = []
        for pose_stamped in self.path.poses:
            px = pose_stamped.pose.position.x
            py = pose_stamped.pose.position.y
            distances.append((px - rx)**2 + (py - ry)**2)
        
        closest_idx = np.argmin(distances)

        for i in range(num_poses):
            idx = (closest_idx + i) % num_poses
            pose = self.path.poses[idx].pose.position
            
            dist = np.sqrt((pose.x - rx)**2 + (pose.y - ry)**2)

            if dist >= self.lookahead_distance:
                self.last_index = idx
                return pose
        
        return self.path.poses[(closest_idx + 1) % num_poses].pose.position
    
def main(args=None):
    rclpy.init(args=args)

    controller = MobrobController()

    rclpy.spin(controller)


    controller.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()