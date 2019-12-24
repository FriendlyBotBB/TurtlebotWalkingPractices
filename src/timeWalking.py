#! /usr/bin/python

import rospy
import threading
from  geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan

rospy.init_node('burak_node')

publisher_turtle1 = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size = 1)

a=0
movement = Twist()
girsinMiTF = 0
girsinMiMB = 0
girsinMiTA = 0

movement.linear.x = 0.3
movement.linear.y = 0.0
movement.linear.z = 0.0
movement.angular.x = 0.0
movement.angular.y = 0.0
movement.angular.z = 0.0

def turningFirst():
	print 'turningFirst'
	global girsinMiTF
	if girsinMiTF == 1:
		girsinMiTF = 0
		return
	girsinMiTF = 1
	movement.angular.z = 0.3
	timer = threading.Timer(4.0, moveBit) 
	timer.start()

def moveBit():
	print 'moveBit'
	global girsinMiMB
	if girsinMiMB == 1:
		girsinMiMB = 0
		return
	girsinMiMB = 1
	movement.angular.z = 0.0
	movement.linear.x = 0.3
	timer = threading.Timer(5.0, turningAgain) 
	timer.start()

def turningAgain():
	print 'turningAgain'
	global girsinMiTA
	if girsinMiTA == 1:
		girsinMiTA = 0
		return
	girsinMiTA = 1
	movement.linear.x = 0.0
 	movement.angular.z = -0.3
	timer = threading.Timer(4.0, moveOrTurning) 
	timer.start()

def moveOrTurning():
	print 'moveOrTurning'
	movement.angular.z = 0.0
	movement.linear.x = 0.3

def mover(data):
	for mesafe in data.ranges:
		if(mesafe < 0.8 ):
			movement.linear.x = 0.0
			turningFirst()

if __name__ == '__main__':
	rate = rospy.Rate(10)
	rospy.Subscriber("/scan",LaserScan,mover)
   	while not rospy.is_shutdown():
		publisher_turtle1.publish(movement) 
		rate.sleep()
	rospy.spin()


