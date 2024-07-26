import rclpy
import message_filters
from std_msgs.msg import String
from rclpy.node import Node
import csv

class Syncer(Node):
    def __init__(self):
        super().__init__("syncer")
        Compass_hdg = message_filters.Subscriber(self, String, "/mavros/global_position/compass_hdg") #create sub for each topic
        Global = message_filters.Subscriber(self, String, "/mavros/global_position/global")
        Gp_lp_offset = message_filters.Subscriber(self, String, "/mavros/global_position/gp_lp_offset")
        Gp_orgin = message_filters.Subscriber(self, String, "/mavros/global_position/gp_orgin")
        Local = message_filters.Subscriber(self, String, "/mavros/global_position/local")
        Fix = message_filters.Subscriber(self, String, "/mavros/global_position/raw/fix")
        Gps_vel = message_filters.Subscriber(self, String, "/mavros/global_position/raw/gps_vel")
        Satellites = message_filters.Subscriber(self, String, "/mavros/global_position/raw/satellites")
        Rel_alt = message_filters.Subscriber(self, String, "/mavros/global_position/rel_alt")
        Accel = message_filters.Subscriber(self, String, "/mavros/local_position/accel")
        Odom = message_filters.Subscriber(self, String, "/mavros/local_position/odom")
        Pose = message_filters.Subscriber(self, String, "/mavros/local_position/pose")
        Pose_cov = message_filters.Subscriber(self, String, "/mavros/local_position/pose_cov")
        Velocity_body = message_filters.Subscriber(self, String, "/mavros/local_position/velocity_body")
        Velocity_body_cov = message_filters.Subscriber(self, String, "/mavros/local_position/velocity_body_cov")
        Velocity_local = message_filters.Subscriber(self, String, "/mavros/local_position/velocity_local")

        self.ts = message_filters.ApproximateTimeSynchronizer([Compass_hdg, Global, Gp_lp_offset, Gp_orgin, Local, Fix, Gps_vel, Satellites, Rel_alt, Accel, Odom, Pose, Pose_cov, Velocity_body, Velocity_body_cov, Velocity_local], 10, 0.5, allow_headerless=True)
        self.ts.registerCallback(self.callback)

    def callback(self, compass_hdg, Globals, Gp_lp_offset, Gp_orgin, Local, Fix, Gps_vel, Satellites, Rel_alt, Accel, Odom, Pose, Pose_cov, Velocity_body, Velocity_body_cov, Velocity_local):
        Compass_hdg_msg = str(compass_hdg) #convert message type to string
        Global_msg = str(Globals)
        Gp_lp_offset_msg = str(Gp_lp_offset)
        Gp_orgin_msg = str(Gp_orgin)
        Local_msg = str(Local)
        Fix_msg = str(Fix)
        Gps_vel_msg = str(Gps_vel)
        Satellites_msg = str(Satellites)
        Rel_alt_msg = str(Rel_alt)
        Accel_msg = str(Accel)
        Odom_msg = str(Odom)
        Pose_msg = str(Pose)
        Pose_cov_msg = str(Pose_cov)
        Velocity_body_msg = str(Velocity_body)
        Velocity_body_cov_msg = str(Velocity_body_cov)
        Velocity_local_msg = str(Velocity_local)

        fields = [Compass_hdg_msg, Global_msg, Gp_lp_offset_msg, Gp_orgin_msg, Local_msg, Fix_msg, Gps_vel_msg, Satellites_msg, Rel_alt_msg, Accel_msg, Odom_msg, Pose_msg, Pose_cov_msg, Velocity_body_msg, Velocity_body_cov_msg, Velocity_local_msg] #slice and tailor line for csv, cut off leading and trailing info
        with open("/home/icebergasv/logged.csv", 'a') as file:
            csv.writer(file).writerow(fields)

def main():
    with open("/home/icebergasv/logged.csv", 'a') as file:
        titlerow = ["Compass_hdg_msg", "Global_msg", "Gp_lp_offset_msg", "Gp_orgin_msg", "Local_msg", "Fix_msg", "Gps_vel_msg", "Satellites_msg", "Rel_alt_msg", "Accel_msg", "Odom_msg", "Pose_msg", "Pose_cov_msg", "Velocity_body_msg", "Velocity_body_cov_msg", "Velocity_local_msg"]
        csv.writer(file).writerow(titlerow)
    rclpy.init()
    syncer = Syncer()
    rclpy.spin(syncer)

    syncer.destroy_node()
    rclpy.shutdown()