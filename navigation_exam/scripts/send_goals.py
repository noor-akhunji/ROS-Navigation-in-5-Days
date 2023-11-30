#!/usr/bin/env python  

import os
import sys
import rospy
import rospkg
import rosparam
import actionlib
from move_base_msgs.msg import MoveBaseAction ,MoveBaseGoal, MoveBaseResult

rospy.init_node('husky_send_golas')

saved_loc_path = rospkg.RosPack().get_path('navigation_exam') + '/config/saved_loc.yaml'
os.system('rosparam load ' + saved_loc_path)
client =  actionlib.SimpleActionClient('/move_base', MoveBaseAction)
client.wait_for_server()
rospy.loginfo('move_base action server found.')

saved_points = ('point1', 'point2')

def feedback_cb(feedback):
    return

def send_goal(label):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.position.x = rosparam.get_param('/' + label +'/position/x')
    goal.target_pose.pose.position.y = rosparam.get_param('/' + label +'/position/y')
    goal.target_pose.pose.position.z = rosparam.get_param('/' + label +'/position/z')
    goal.target_pose.pose.orientation.x = rosparam.get_param('/' + label +'/orientation/x')
    goal.target_pose.pose.orientation.y = rosparam.get_param('/' + label +'/orientation/y')
    goal.target_pose.pose.orientation.z = rosparam.get_param('/' + label +'/orientation/z')
    goal.target_pose.pose.orientation.w = rosparam.get_param('/' + label +'/orientation/w')
    client.send_goal(goal, feedback_cb=feedback_cb)

no_poses = len(saved_points)
i = 0
while True:
    try:
        label = saved_points[i % no_poses]
        rospy.loginfo('Sending goal: ' + label)
        send_goal(label)
        rospy.loginfo('Waiting to reach Goal.')
        client.wait_for_result(rospy.Duration(100))
        rospy.loginfo('Goal Reached')
        rospy.sleep(1.)
        i += 1
    except:
        client.cancel_all_goals()
        rospy.loginfo('Exiting now.')
        sys.exit(0)