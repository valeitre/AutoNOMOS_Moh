#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int16

st_pub = None
sp_pub = None

def clbk_laser(msg):
    # 360 / 10 = 36
    distance = 6 #set maximun distance (m)
    regions = {
        'rigth': min(min(msg.ranges[0:35]), distance),
        'fright': min(min(msg.ranges[36:71]), distance),
        'front': min(min(msg.ranges[72:107]), distance),
        'fleft': min(min(msg.ranges[108:143]), distance),
        'left': min(min(msg.ranges[144:179]), distance),
   #     'back_rigth': min(min(msg.ranges[180:215]), distance),
    #    'back_frigth': min(min(msg.ranges[216:251]), distance),
     #   'back_front': min(min(msg.ranges[252:287]), distance),
      #  'back_fleft': min(min(msg.ranges[288:323]), distance),
       # 'back_left': min(min(msg.ranges[324:359]), distance),
    }
    take_action(regions)
  #  rospy.loginfo(pub)

def take_action(regions):
    st_msg = Int16() #for steering message
    sp_msg = Int16() #for speed message
    
    steer = 90
    speed = 0 #initialize speed forward
        
    st_msg.data = steer
    sp_msg.data = speed
        
    st_pub.publish(st_msg)
    sp_pub.publish(sp_msg)
       
    rospy.loginfo(st_msg.data) #printing steer value
    rospy.loginfo(sp_msg.data) #printing speed value


def main():
    global sp_pub
    global st_pub
    
    rospy.init_node('stop_car')
    st_pub = rospy.Publisher('/AutoNOMOS_mini/manual_control/steering', Int16, queue_size=1)
    sp_pub = rospy.Publisher('/AutoNOMOS_mini/manual_control/speed', Int16, queue_size=1) 
    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    rospy.spin()

   
if __name__ == '__main__':
    main()
