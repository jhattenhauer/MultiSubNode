import rclpy
import message_filters
from std_msgs.msg import String
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSDurabilityPolicy

class Syncer(Node):
    def __init__(self):
        super().__init__("syncer")
        message1 = message_filters.Subscriber(
            self, String, "topic1")
        message2 = message_filters.Subscriber(
            self, String, "topic2")

        queue_size = 10
        delay = 1.0
        self.ts = message_filters.ApproximateTimeSynchronizer(
            [message1, message2], queue_size, delay)
        self.ts.registerCallback(self._cb)

    def _cb(self, msg_1, msg_2):
        self.get_logger().info("Received messages!!")
        self.get_logger().info(f"from Foo: {msg_1}")
        self.get_logger().info(f"from Bar: {msg_2}")

def main():
    rclpy.init()
    syncer = Syncer()
    rclpy.spin(syncer)

    syncer.destroy_node()
    rclpy.shutdown()
