#!/usr/bin/env python2

########
#Name: apriltag_manager.py
#
#Purpose: Recieves tag id from camera node then published it to robot_controller.py which passes it on to the navigation manaer.
#
# Author: Faizan Niazi <fniazi@ucsd.edu>, Pragna Guntupalli <sguntupalli@ucsd.edu>
#
#Acknowledgements: ROS1 documentation, April Laboratory documentation
#
#Date: 07 June 2026
#########

import rospy
from apriltag_ros.msg import AprilTagDetectionArray

class AprilTagManager:
    def __init__(self):
        self.current_tag = None

        rospy.Subscriber(
            "/tag_detections", 
            AprilTagDetectionArray, 
            self.tag_callback
        )
    
    def tag_callback(self, msg):
        if msg.detections:
            tag_id = msg.detections[0].id
            if tag_id:
                self.current_tag = tag_id[0]
                rospy.loginfo("AprilTag detected")
        else:
            self.current_tag = None

    
    def get_current_tag(self):
        return self.current_tag