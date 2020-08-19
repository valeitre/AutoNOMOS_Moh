#! /usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16

pub = None

def clbk_laser(msg):
    # 360 / 10 = 36
    regions = {
        'rigth': min(min(msg.ranges[0:35]), 6),
        'fright': min(min(msg.ranges[36:71]), 6),
        'front': min(min(msg.ranges[72:107]), 6),
        'fleft': min(min(msg.ranges[108:143]), 6),
        'left': min(min(msg.ranges[144:179]), 6),
   #     '': min(min(msg.ranges[180:215]), 6),
    #    '': min(min(msg.ranges[216:251]), 6),
     #   '': min(min(msg.ranges[252:287]), 6),
      #  '': min(min(msg.ranges[288:323]), 6),
       # '': min(min(msg.ranges[324:359]), 6),
    }
    take_action(regions)
    rospy.loginfo(pub)

def take_action(regions):
    msg = Int16()
    msg.data = 0
    pub.publish(msg)
    rate = rospy.Rate(3)
    while not rospy.is_shutdown():
    	pub.publish(msg)
    	msg.data = 0
    	rospy.loginfo(pub)
    	rate.sleep()
 
 
def main():
    global pub
    rospy.init_node('reading_laser')
    pub = rospy.Publisher('/AutoNOMOS_mini/manual_control/speed', Int16, queue_size=1) 
    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    rospy.spin()

   
if __name__ == '__main__':
    main()
