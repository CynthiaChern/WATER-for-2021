#!/usr/bin/env python
import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
w/s  :increase/decrease linear speed 0.01
a/d  :increase/decrease angular speed 0.1
---------------------------
x    :speed to 0
CTRL-C to quit
"""

moveBindings = {
		'w':(0.02,0,0,0),
		's':(-0.02,0,0,0),
		'a':(0,0,0,0.1),
		'd':(0,0,0,-0.1),
	       }

speedBindings={
		'x':(0,0,0,0),
	      }

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key


def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)
	
	pub = rospy.Publisher('cmd_vel_1', Twist, queue_size = 1)
	rospy.init_node('teleop_twist_keyboard')

	speed = rospy.get_param("~speed", 0)
	turn = rospy.get_param("~turn", 0)
	x = 0
	y = 0
	z = 0
	th = 0
	status = 0

	try:
		print msg
		print vels(speed,turn)
		while(1):
			key = getKey()
			if key in moveBindings.keys():
				x = x+moveBindings[key][0]
				y = y+moveBindings[key][1]
				z = z+moveBindings[key][2]
				th = th+moveBindings[key][3]
				print vels(x,th)
			elif key in speedBindings.keys():
				x = 0
				y = 0
				z = 0
				th = 0
				print vels(x,th)
			else:
				x = 0
				y = 0
				z = 0
				th = 0
				if (key == '\x03'):
					break

			twist = Twist()
			twist.linear.x = x; twist.linear.y = y; twist.linear.z = z;
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th;
			pub.publish(twist)

	except:
		print e

	finally:
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pub.publish(twist)

    		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


