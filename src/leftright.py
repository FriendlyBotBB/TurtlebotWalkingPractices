#! /usr/bin/python

import rospy
import threading
import random
import math
from  geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

rospy.init_node('burak_node')

publisher_turtlebot = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size = 1)

yon = 1
bakilanYon = 0
yer = Odometry()
geriDonus = 0
max_value = 0
movement = Twist()

movement.linear.x = 0.4
movement.linear.y = 0.0
movement.linear.z = 0.0
movement.angular.x = 0.0
movement.angular.y = 0.0
movement.angular.z = 0.0

def mover(data):
	global yon
	global yer
	global bakilanYon
	global geriDonus
	global max_value
	donmek = 1
	for mesafe in data.ranges:
		if(mesafe < 0.6):
			if(mesafe > max_value):
				max_value = mesafe
			movement.linear.x = 0.0
			movement.angular.z = yon * 0.8
			donmek = 0
	simdikiYon = abs(yer.pose.pose.orientation.z)
	oncekiYon = abs(bakilanYon)
	if(abs(simdikiYon - oncekiYon) > 0.40 and geriDonus == 0):
		for mesafe in data.ranges:
			print(mesafe < 2 and mesafe != 'nan')
			print(mesafe)
			if(mesafe < 2 and mesafe != 'nan'):
				geriDonus = 1
				yon = -yon
	if(donmek == 1):
		bakilanYon = yer.pose.pose.orientation.z
		yon = randomPlusOrNegate()
		movement.linear.x = 0.4
		movement.angular.z = 0.0
		geriDonus = 0

def randomPlusOrNegate():
	a = random.random()
	if(a > 0.5):
		return 1
	else:
		return -1


def yerBilgisi(data):
	global yer
	yer = data


if __name__ == '__main__':
	rate = rospy.Rate(10)
	rospy.Subscriber("/scan",LaserScan,mover)
	rospy.Subscriber("/odom",Odometry,yerBilgisi)
   	while not rospy.is_shutdown():
		publisher_turtlebot.publish(movement) 
		rate.sleep()
	rospy.spin()


