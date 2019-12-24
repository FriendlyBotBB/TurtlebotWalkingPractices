#! /usr/bin/python

import rospy
import threading
from  geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Quaternion

rospy.init_node('burak_node')

publisher_turtle1 = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size = 1)

yerim = Odometry()
yonum = 0
donuyorMu = 0
a = 0
movement = Twist()

movement.linear.x = 0.3
movement.linear.y = 0.0
movement.linear.z = 0.0
movement.angular.x = 0.0
movement.angular.y = 0.0
movement.angular.z = 0.0

def mover(data):
	global yerim
	global yonum
	global donuyorMu
	controller()
	for mesafe in data.ranges:
		if(mesafe < 0.8 and donuyorMu == 0):
			movement.linear.x = 0.0
			yonum = yerim.pose.pose.orientation.z
			donuyorMu = 1
			movement.angular.z = 0.3

def controller():
	global yerim
	global yonum
	global donuyorMu
	fark = yonum - yerim.pose.pose.orientation.w
	if((fark > 0.30) or (fark < -0.30)) and donuyorMu == 1:
		donuyorMu = 0
		movement.angular.z = 0.0
		movement.linear.x = 0.3
	

def yer(data):
	global yerim
	global a
	yerim = data
	if(a==1):
		print(yerim)
		a=10

if __name__ == '__main__':
	rate = rospy.Rate(10)
	rospy.Subscriber("/scan",LaserScan,mover)
	rospy.Subscriber("/odom",Odometry,yer)
   	while not rospy.is_shutdown():
		publisher_turtle1.publish(movement) 
		rate.sleep()
	rospy.spin()


