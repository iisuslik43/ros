#!/usr/bin/python3
import rospy
import numpy as np
from datetime import datetime, timedelta
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist


class Chaser:
    def __init__(self):
        self.pub = rospy.Publisher('/chaser/cmd_vel', Twist, queue_size=1)
        self.chaser_pose = None
        # self.last_time = None

    def turtle1PoseChanged(self, turtle1_pose):
        if self.chaser_pose is None:
            return
        move = Twist()
        move.linear.x = 1
        move.angular.z =  np.arctan((turtle1_pose.y - self.chaser_pose.y) / (turtle1_pose.x - self.chaser_pose.x))
        if self.chaser_pose.x > turtle1_pose.x:
            move.angular.z += np.pi
        if move.angular.z > np.pi:
            move.angular.z -= 2 * np.pi
        rospy.loginfo(f'{move.angular.z}  {self.chaser_pose.theta}')
        move.angular.z -= self.chaser_pose.theta
        self.pub.publish(move)


    def chaserPoseChanged(self, msg):
        self.chaser_pose = msg

    def run(self):
        rospy.Subscriber('/turtle1/pose', Pose, self.turtle1PoseChanged)
        rospy.Subscriber('/chaser/pose', Pose, self.chaserPoseChanged)
        rospy.spin()



rospy.init_node('chaser_node')
chaser = Chaser()
chaser.run()