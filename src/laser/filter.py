#!/usr/bin/python3
import rospy
from sensor_msgs.msg import LaserScan


pub = rospy.Publisher('/filtered_scan', LaserScan, queue_size=10)
DELTA = 0.1
WINDOW_SIZE = 3

def callback(msg):
    n = len(msg.ranges)
    good = [False] * n
    for i in range(n):
        window = msg.ranges[max(i - WINDOW_SIZE, 0): min(i + 1 + WINDOW_SIZE, n)]
        if (max(window) - min(window)) < DELTA:
            for j in range(max(i - WINDOW_SIZE, 0), min(i + 1 + WINDOW_SIZE, n)):
                good[j] = True
    msg.ranges = [v for (i, v) in enumerate(msg.ranges)
                    if good[i]]

    rospy.loginfo(f'Filtered {int((n - len(msg.ranges)) * 100 / n)}% points')
    pub.publish(msg)

rospy.init_node('laser_filter')
sub = rospy.Subscriber('/base_scan', LaserScan, callback)
rospy.spin()