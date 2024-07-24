import rclpy
import message_filters
from std_msgs.msg import String
from rclpy.node import Node


class Syncer(Node):
    def __init__(self):
        super().__init__("syncer")
        message1 = message_filters.Subscriber(self, "topic1", String)
        message2 = message_filters.Subscriber(self, "topic2", String)
    
        self.ts = message_filters.ApproximateTimeSynchronizer(
            [message1, message2], 10)
        self.ts.registerCallback(self._cb)

    def _cb(self, msg_mes1, msg_mes2):
        self.get_logger().info("Received messages!!")
        self.get_logger().info(f"from Foo: {msg_mes1}")
        self.get_logger().info(f"from Bar: {msg_mes2}")

def main():
    rclpy.init()
    syncer = Syncer()

    executor = rclpy.executors.MultiThreadedExecutor(3)
    executor.add_node(syncer)
    executor.spin()

    syncer.destroy_node()
    rclpy.shutdown()
