#-------------------------------------------------------------------------------#
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from tf2_ros import Buffer, TransformListener
import pygame
import sys
#-------------------------------------------------------------------------------#


class TVVisualizer(Node):
    def __init__(self):
        super().__init__('tv_visualizer')

        self.robname = self.declare_parameter('robname', 'rob1').get_parameter_value().string_value

        # pygaym setup
        pygame.init()

        self.screen_res = (2560, 1440)
        self.screen = pygame.display.set_mode(self.screen_res, pygame.FULLSCREEN)
        pygame.display.set_caption("Robot Path Overlay")

        # scqaling
        self.scale = 100.0 # pixels per world unit
        #self.offset = (self.screen_res[0] // 2, self.screen_res[1] // 2) # if center is 0,0
        self.offset = (0,0)

        # ROS
        self.path_data = []
        self.robot_pos = (0,0)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.path_sub = self.create_subscription(Path, f'/{self.robname}/path', self.path_callback, 10)

        # teima
        self.timer = self.create_timer(0.5, self.update_display)
    

    def path_callback(self, msg):
        for p in msg.poses:
            self.path_data.append((p.pose.position.x, p.pose.position.y))
    
    def world_to_pixel(self, x, y):
        px = int(x * self.scale + self.offset[0])
        py = int(self.screen_res[1] - (y * self.scale + self.offset[1]))
        return (px, py)
    
    def update_display(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Try to get robot position via TF
        try:
            now = rclpy.time.Time()
            trans = self.tf_buffer.lookup_transform('map', self.robname, now)
            self.robot_pos = (trans.transform.translation.x, trans.transform.translation.y)
        except Exception:
            pass

        # draw
        self.screen.fill((0, 0, 0)) # Black background

        # draw path
        if len(self.path_data) > 1:
            points = [self.world_to_pixel(x, y) for x, y in self.path_data]
            pygame.draw.lines(self.screen, (255, 255, 255), False, points, 5)

        # Draw Robot Position (Red circle)
        rx, ry = self.world_to_pixel(self.robot_pos[0], self.robot_pos[1])
        pygame.draw.circle(self.screen, (255, 0, 0), (rx, ry), 15)

        pygame.display.flip()

def main():
    rclpy.init()
    tvviz = TVVisualizer()
    try:
        rclpy.spin(tvviz)
    except SystemExit:
        pass
    rclpy.shutdown()