#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
import newpath
x=0.0
y=0.0
theta =0.0

def newOdom(msg):
    
    global x
    global y 
    global theta
    x= msg.pose.pose.position.x
    y= msg.pose.pose.position.y
    
    rot_q = msg.pose.pose.orientation
    (roll,pitch,theta)= euler_from_quaternion([rot_q.x,rot_q.y,rot_q.z,rot_q.w])
    

rospy.init_node("speed_controller")

sub = rospy.Subscriber("/odom_comb",Odometry,newOdom)
pub = rospy.Publisher("/cmd_vel",Twist,queue_size=1)
speed = Twist()
r = rospy.Rate(4)
goal= Point()

goals=newpath.getRuta()
goal.x=goals[0][0]
goal.y=goals[0][1]
cont=1
while not rospy.is_shutdown():
    
    inc_x = goal.x -x
    inc_y= goal.y - y
    angle_to_goal = atan2(inc_y, inc_x)
    
    if abs(angle_to_goal -theta ) > 0.1:
        speed.linear.x=0.0
        speed.angular.z = 0.3
    else:
	goal.x=goals[cont][0]
	goal.y=goals[cont][1]
	cont = cont+1
        #speed.linear.x=0.5
        #speed.angular.z = 0.0  
    
      
    pub.publish(speed)
    r.sleep()
