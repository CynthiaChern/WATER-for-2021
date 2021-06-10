#!/usr/bin/env python
# encoding:utf-8
import roslib
import rospy

import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError

import numpy as np

from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
from darknet_ros_msgs.msg import BoundingBox
from darknet_ros_msgs.msg import BoundingBoxes
from geometry_msgs.msg import Twist
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Image


class BodyCheck:
    def __init__(self):
        self.yolo_sub_ = rospy.Subscriber("/darknet_ros/bounding_boxes", BoundingBoxes, self.yoloCallback)
        self.cam_info_sub_ = rospy.Subscriber("/water_astra_rgbd/depth/camera_info", CameraInfo, self.caminfoCallback)
        self.pts_sub_ = rospy.Subscriber("/water_astra_rgbd/rgb/image_raw", Image, self.imgCallback)
        self.follow_name_ = rospy.get_param("/follow/name", "chair")
        self.speed_pub_ = rospy.Publisher("/cmd_vel", Twist, tcp_nodelay=True)
        self.max_ang_speed = 0.3
        self.max_lin_speed = 0.5

        self.tar_in_sight = False        
        self.tar_mid_x = 0
        self.tar_mid_y = 0

        self.gain_cam_info = False
        self.cam_c = []
        self.cam_f = []

        self.speed = Twist()
        self.speed.angular.x = 0.0
        self.speed.angular.y = 0.0
        self.speed.linear.y = 0.0
        self.speed.linear.z = 0.0

        self.cv_bridge = CvBridge()

        # 640*480

    def caminfoCallback(self, msg):
        # msg = CameraInfo()
        # fx, cx ; fy, cy
        self.cam_f = [msg.P[0], msg.P[5]]
        self.cam_c = [msg.P[2], msg.P[6]]
        self.gain_cam_info = True
        print(self.gain_cam_info)
        self.cam_info_sub_.unregister()

    def imgCallback(self, msg):
        if not self.gain_cam_info:
            return
        # try:
        #     depth_image = self.cv_bridge.imgmsg_to_cv2(msg, "passthrough")
        #     depth_array = np.array(depth_image, dtype=np.float32)
        #     print(depth_array.shape)

        #     depth = depth_array[self.tar_mid_y, self.tar_mid_x]
        #     print(depth)
        # except CvBridgeError, e:
        #     print e


    def yoloCallback(self, msg):
        # msg = BoundingBoxes()
        find_goal = False
        self.speed.linear.x = 0.0
        self.speed.angular.z = 0.0

        for bounding_box in msg.bounding_boxes:
            if bounding_box.Class == self.follow_name_:
                find_goal = True
                x_rang = float(bounding_box.xmax) - float(bounding_box.xmin)
                y_rang = float(bounding_box.ymax) - float(bounding_box.ymin)
                print("Find Goal")
                self.tar_mid_x = int(0.5*(float(bounding_box.xmax) + float(bounding_box.xmin)))
                self.tar_mid_y = int(0.5*(float(bounding_box.ymax) + float(bounding_box.ymin)))
                if abs(self.tar_mid_x-320.0) < 30.0:
                    self.speed.angular.z = 0.0
                    pass
                else:
                    self.speed.angular.z = (320.0 - self.tar_mid_x)/(320.0)*self.max_ang_speed

                if x_rang*y_rang > 0.30*(640*480):
                    self.speed.linear.x = 0.0
                elif x_rang*y_rang > (0.10*640*480):
                    rate = (0.10*640.0*480.0)/(x_rang*y_rang)
                    self.speed.linear.x = self.max_lin_speed*rate
                else:
                    self.speed.linear.x = self.max_lin_speed
                break
        if not find_goal:
            pass
            if self.tar_mid_x > 320:
                self.speed.angular.z = -self.max_ang_speed
            else:
                self.speed.angular.z = self.max_ang_speed
        print(self.speed)
        self.speed_pub_.publish(self.speed)
if __name__ == "__main__":
    rospy.init_node('follow_node', anonymous=True)
    body = BodyCheck()
    print("!!!")
    rospy.spin()
