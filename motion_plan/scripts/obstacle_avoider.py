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
    #rospy.loginfo(regions)
    take_action(regions)
    

def take_action(regions):
    st_msg = Int16() #for steering message
    sp_msg = Int16() #for speed message
    #st_msg.data = 90 #initialize steering to center
    speed = -100 #initialize speed forward
    
    #pub.publish(st_msg) #sending msg to steering topic
    #pub.publish(sp_msg) #sending msg to speed topic
    rate = rospy.Rate(3) #printing 3 msgs in 1s
    
    state_description = ''
    
    #while not rospy.is_shutdown():
    if regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] > 1:
        state_description = 'case 1 - nothing'
        steer = 90 #go forward there isn't obstacules
        speed = -300 #you can go fast

    elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] > 1:
        state_description = 'case 2 - front'
        steer = 30 #go high rigth or left
        speed = -200

    elif regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 3 - fright'
        steer = 120 #go low left
        speed = -200

    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 4 - fleft'
        steer = 60 #go low rigth
        speed = -200

    elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 5 - front and fright'
        steer = 180 #go high left
        speed = -200

    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 6 - front and fleft'
        steer = 0 #go high rigth
        speed = -200

    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 7 - front and fleft and fright'
        steer = 180 #go maximun rigth or left
        speed = -100 #and slowdown

    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 8 - fleft and fright'
        steer = 0 #go maximun rigth or left
        speed = -100 #and slowdown

    else:
        state_description = 'unknown case'
        rospy.loginfo(regions) #printing laser reading regions
    
    rospy.loginfo(state_description)
    rospy.loginfo(regions)
    st_msg.data = steer
    sp_msg.data = speed
        
    st_pub.publish(st_msg)
    sp_pub.publish(sp_msg)
    #rospy.loginfo(st_msg.data) #printing steer value
 #   rate.sleep()
 
 
def main():
    global sp_pub
    global st_pub
    
    rospy.init_node('obstacule_avoid')
    st_pub = rospy.Publisher('/AutoNOMOS_mini/manual_control/steering', Int16, queue_size=1)
    sp_pub = rospy.Publisher('/AutoNOMOS_mini/manual_control/speed', Int16, queue_size=1) 
    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    rospy.spin()

   
if __name__ == '__main__':
    main()
