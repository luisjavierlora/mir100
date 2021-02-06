#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from sensor_msgs.msg import JointState
from sensor_msgs.msg import Joy


from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
x=0.0
y=0.0
theta =0.0



class Joystick(object):
	#class Joysitck
    def __init__(self):
        self.axes = 6*[0.,]
        self.buttons = 6*[0.,]
        rospy.Subscriber("/joy", Joy, self.callback)

    def callback(self, msg):
        self.axes = msg.axes
        self.buttons = msg.buttons

#initialize node
rospy.init_node("test1")
joystick = Joystick()


pub = rospy.Publisher("/cmd_vel",Twist,queue_size=1)
speed = Twist()
r = rospy.Rate(20)


while not rospy.is_shutdown():
    
    
	#Movement Joystick
	xaux=joystick.axes[1]
	theta_aux=joystick.axes[3]

	
	print(xaux)

	if(xaux>0):
		speed.linear.x=0.5

	elif(xaux==0):
		speed.linear.x=0	
	else:
		speed.linear.x=-0.5


	if(theta_aux>0):
		speed.angular.z = 0.3

	elif(theta_aux==0):
		speed.angular.z = 0.0	
	else:
		speed.angular.z = -0.3

        
	pub.publish(speed)
	r.sleep()
    



