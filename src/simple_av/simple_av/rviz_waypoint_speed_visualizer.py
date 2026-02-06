import rclpy
from rclpy.node import Node
import math

from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import Marker, MarkerArray
from simple_av_msgs.msg import PlanningInternalMissionPlanMsg
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy


class WaypointSpeedVisualizer(Node):
    def __init__(self):
        super().__init__('rviz_waypoint_speed_visualizer')

        self.declare_parameter('mission_plan_topic', '/simple_av/motion_planning/trajectory')
        self.declare_parameter('marker_topic', '/waypoint_speed_markers')
        self.declare_parameter('frame_id', 'map')
        self.declare_parameter('point_scale', 1.0)
        self.declare_parameter('text_scale', 0.9)
        self.declare_parameter('text_height', 1.6)
        self.declare_parameter('text_offset_x', 0.6)
        self.declare_parameter('text_offset_y', 0.0)
        self.declare_parameter('id_offset_x', 1.2)
        self.declare_parameter('id_offset_y', 0.0)
        self.declare_parameter('id_text_scale', 0.7)
        self.declare_parameter('marker_stride', 1)
        self.declare_parameter('text_stride', 1)
        self.declare_parameter('max_speed', 11.0)
        self.declare_parameter('min_speed', 0.0)
        self.declare_parameter('max_lateral_accel', 4.0)
        self.declare_parameter('curvature_gain', 1.0)
        self.declare_parameter('curve_epsilon', 1e-3)
        self.declare_parameter('marker_alpha', 0.9)

        mission_plan_topic = self.get_parameter('mission_plan_topic').get_parameter_value().string_value
        marker_topic = self.get_parameter('marker_topic').get_parameter_value().string_value

        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )

        self.subscription = self.create_subscription(
            PlanningInternalMissionPlanMsg,
            mission_plan_topic,
            self.mission_plan_callback,
            qos_profile
        )

        self.publisher = self.create_publisher(MarkerArray, marker_topic, qos_profile)

        self.get_logger().info(
            f"Waypoint speed visualizer listening on {mission_plan_topic} and publishing {marker_topic}."
        )

    def compute_speed(self, curve):
        max_speed = self.get_parameter('max_speed').get_parameter_value().double_value
        min_speed = self.get_parameter('min_speed').get_parameter_value().double_value
        max_lateral_accel = self.get_parameter('max_lateral_accel').get_parameter_value().double_value
        curvature_gain = self.get_parameter('curvature_gain').get_parameter_value().double_value
        curve_epsilon = self.get_parameter('curve_epsilon').get_parameter_value().double_value

        if curve <= curve_epsilon:
            speed = max_speed
        else:
            effective_lat_accel = max_lateral_accel * max(curvature_gain, 0.0)
            speed = min(max_speed, math.sqrt(effective_lat_accel / max(curve, curve_epsilon)))

        return max(min_speed, speed)

    def speed_to_color(self, speed):
        max_speed = self.get_parameter('max_speed').get_parameter_value().double_value
        min_speed = self.get_parameter('min_speed').get_parameter_value().double_value
        alpha = self.get_parameter('marker_alpha').get_parameter_value().double_value

        if max_speed <= min_speed:
            t = 0.0
        else:
            t = (speed - min_speed) / (max_speed - min_speed)
        t = max(0.0, min(1.0, t))

        return ColorRGBA(r=t, g=0.2, b=1.0 - t, a=alpha)

    def mission_plan_callback(self, msg: PlanningInternalMissionPlanMsg):
        frame_id = self.get_parameter('frame_id').get_parameter_value().string_value
        point_scale = self.get_parameter('point_scale').get_parameter_value().double_value
        text_scale = self.get_parameter('text_scale').get_parameter_value().double_value
        text_height = self.get_parameter('text_height').get_parameter_value().double_value
        text_offset_x = self.get_parameter('text_offset_x').get_parameter_value().double_value
        text_offset_y = self.get_parameter('text_offset_y').get_parameter_value().double_value
        id_offset_x = self.get_parameter('id_offset_x').get_parameter_value().double_value
        id_offset_y = self.get_parameter('id_offset_y').get_parameter_value().double_value
        id_text_scale = self.get_parameter('id_text_scale').get_parameter_value().double_value
        marker_stride = self.get_parameter('marker_stride').get_parameter_value().integer_value
        text_stride = self.get_parameter('text_stride').get_parameter_value().integer_value

        marker_stride = max(1, marker_stride)
        text_stride = max(1, text_stride)

        now = self.get_clock().now().to_msg()
        marker_array = MarkerArray()

        clear_marker = Marker()
        clear_marker.action = Marker.DELETEALL
        marker_array.markers.append(clear_marker)

        points_marker = Marker()
        points_marker.header.frame_id = frame_id
        points_marker.header.stamp = now
        points_marker.ns = 'waypoint_speed'
        points_marker.id = 0
        points_marker.type = Marker.SPHERE_LIST
        points_marker.action = Marker.ADD
        points_marker.pose.orientation.w = 1.0
        points_marker.scale.x = point_scale
        points_marker.scale.y = point_scale
        points_marker.scale.z = point_scale
        points_marker.color.a = self.get_parameter('marker_alpha').get_parameter_value().double_value

        text_id = 1
        for i, wp in enumerate(msg.path):
            if i % marker_stride != 0:
                continue

            speed = self.compute_speed(wp.curve)
            color = self.speed_to_color(speed)
            points_marker.points.append(Point(x=wp.waypoint.x, y=wp.waypoint.y, z=wp.waypoint.z))
            points_marker.colors.append(color)

            if i % text_stride != 0:
                continue

            speed_marker = Marker()
            speed_marker.header.frame_id = frame_id
            speed_marker.header.stamp = now
            speed_marker.ns = 'waypoint_speed_text'
            speed_marker.id = text_id
            speed_marker.type = Marker.TEXT_VIEW_FACING
            speed_marker.action = Marker.ADD
            speed_marker.pose.position = Point(
                x=wp.waypoint.x + text_offset_x,
                y=wp.waypoint.y + text_offset_y,
                z=wp.waypoint.z + text_height
            )
            speed_marker.pose.orientation.w = 1.0
            speed_marker.scale.z = text_scale
            speed_marker.color = color
            speed_marker.text = f"{speed * 3.6:.1f}"
            marker_array.markers.append(speed_marker)
            text_id += 1

            id_marker = Marker()
            id_marker.header.frame_id = frame_id
            id_marker.header.stamp = now
            id_marker.ns = 'waypoint_id_text'
            id_marker.id = text_id
            id_marker.type = Marker.TEXT_VIEW_FACING
            id_marker.action = Marker.ADD
            id_marker.pose.position = Point(
                x=wp.waypoint.x + id_offset_x,
                y=wp.waypoint.y + id_offset_y,
                z=wp.waypoint.z + text_height
            )
            id_marker.pose.orientation.w = 1.0
            id_marker.scale.z = id_text_scale
            id_marker.color.r = 1.0
            id_marker.color.g = 1.0
            id_marker.color.b = 1.0
            id_marker.color.a = 1.0
            id_marker.text = str(i)
            marker_array.markers.append(id_marker)
            text_id += 1

        marker_array.markers.append(points_marker)
        self.publisher.publish(marker_array)


def main(args=None):
    rclpy.init(args=args)
    node = WaypointSpeedVisualizer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
