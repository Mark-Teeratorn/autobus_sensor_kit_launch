#!/usr/bin/env python3
"""
IMU QoS Bridge: Subscribes to MAVROS IMU (BEST_EFFORT) and republishes with RELIABLE QoS
for Autoware's imu_corrector which requires RELIABLE QoS.
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Imu


class ImuQosBridge(Node):
    def __init__(self):
        super().__init__('imu_qos_bridge')

        self.declare_parameter('input_topic', '/sensing/mavros_node/data_raw')
        self.declare_parameter('output_topic', '/sensing/imu/mavros_imu_raw')

        input_topic = self.get_parameter('input_topic').get_parameter_value().string_value
        output_topic = self.get_parameter('output_topic').get_parameter_value().string_value

        # Subscribe with BEST_EFFORT (matches MAVROS)
        sub_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Publish with RELIABLE (matches Autoware imu_corrector)
        pub_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.publisher = self.create_publisher(Imu, output_topic, pub_qos)
        self.subscription = self.create_subscription(Imu, input_topic, self.callback, sub_qos)

        self.get_logger().info(
            f'QoS Bridge: {input_topic} (BEST_EFFORT) -> {output_topic} (RELIABLE)')

    def callback(self, msg):
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ImuQosBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
