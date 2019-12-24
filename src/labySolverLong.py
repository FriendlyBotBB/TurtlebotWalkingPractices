#! /usr/bin/python

import rospy
import threading
import random
from  geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

rospy.init_node('burak_node')

publisher_turtlebot = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size = 1)

yon = 1

movement = Twist()

movement.linear.x = 0.3
movement.linear.y = 0.0
movement.linear.z = 0.0
movement.angular.x = 0.0
movement.angular.y = 0.0
movement.angular.z = 0.0

def mover(data):
	global yon
	global ikile
	donmek = 1
	for mesafe in data.ranges:
		if(mesafe < 0.6):
			movement.linear.x = 0.0
			movement.angular.z = yon * 0.8
			donmek = 0
	if(donmek == 1):
		yon = randomPlusOrNegate()
		movement.linear.x = 0.3
		movement.angular.z = 0.0

def randomPlusOrNegate():
	a = random.random()
	if(a > 0.5):
		return 1
	else:
		return -1


if __name__ == '__main__':
	rate = rospy.Rate(10)
	rospy.Subscriber("/scan",LaserScan,mover)
   	while not rospy.is_shutdown():
		publisher_turtlebot.publish(movement) 
		rate.sleep()
	rospy.spin()


