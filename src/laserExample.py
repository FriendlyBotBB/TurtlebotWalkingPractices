#! /usr/bin/python

import rospy
from  geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

rospy.init_node('burak_node')

publisher_turtlebot = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size = 1)

movement = Twist()

movement.linear.x = 0.4
movement.linear.y = 0.0
movement.linear.z = 0.0
movement.angular.x = 0.0
movement.angular.y = 0.0
movement.angular.z = 0.0

def mover(data):
    for x in data.ranges:
        if(x<1):
            movement.linear.x = 0

if __name__ == '__main__':
    rate = rospy.Rate(10)
    rospy.Subscriber("/scan",LaserScan,mover)
    while not rospy.is_shutdown():
        publisher_turtlebot.publish(movement)
        rate.sleep()
    rospy.spin()


