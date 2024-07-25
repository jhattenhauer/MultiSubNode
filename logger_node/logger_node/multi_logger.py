import rclpy
import message_filters
from std_msgs.msg import String
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSDurabilityPolicy
import csv

class Syncer(Node):
    def __init__(self):
        super().__init__("syncer")
        message1 = message_filters.Subscriber(self, String, "topic1") #create sub for each topic
        message2 = message_filters.Subscriber(self, String, "topic2")

        self.ts = message_filters.ApproximateTimeSynchronizer([message1, message2], 10, 0.5, allow_headerless=True)
        self.ts.registerCallback(self.callback)

    def callback(self, msg_1, msg_2):
        message1 = str(msg_1) #convert message type to string
        message2 = str(msg_2)
        fields = [message1[26:-2], message2[26:-2]] #slice and tailor line for csv, cut off leading and trailing info
        with open("/home/james/Iceberg/MultiSubNode/logged.csv", 'a') as file:
            csv.writer(file).writerow(fields)

def main():
    rclpy.init()
    syncer = Syncer()
    rclpy.spin(syncer)

    syncer.destroy_node()
    rclpy.shutdown()
