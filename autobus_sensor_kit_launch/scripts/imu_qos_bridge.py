#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from sensor_msgs.msg import Imu

class ImuQosBridge(Node):
    def __init__(self):
        super().__init__('imu_qos_bridge')

        self.declare_parameter('input_topic',  '/sensing/gnss/imu/data')
        self.declare_parameter('output_topic', '/sensing/imu/imu_data')

        input_topic  = self.get_parameter('input_topic').get_parameter_value().string_value
        output_topic = self.get_parameter('output_topic').get_parameter_value().string_value

        sub_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        pub_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.publisher_   = self.create_publisher(Imu, output_topic, pub_qos)
        self.subscription = self.create_subscription(Imu, input_topic, self.callback, sub_qos)

        self.get_logger().info(f'IMU QoS Bridge: {input_topic} -> {output_topic}')

    def callback(self, msg):
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ImuQosBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()