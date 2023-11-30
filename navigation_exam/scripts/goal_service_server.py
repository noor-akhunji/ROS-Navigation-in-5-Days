#!/usr/bin/env python  

import os
import rospy
import rospkg
import rosparam
import actionlib
from move_base_msgs.msg import MoveBaseAction ,MoveBaseGoal, MoveBaseResult
from navigation_exam.srv import SendPosition, SendPositionRequest, SendPositionResponse

rospy.init_node('goals_service_server')

saved_loc_path = rospkg.RosPack().get_path('navigation_exam') + '/config/saved_loc.yaml'
os.system('rosparam load ' + saved_loc_path)
client =  actionlib.SimpleActionClient('/move_base', MoveBaseAction)
client.wait_for_server()
rospy.loginfo('move_base action server found.')

def feedback_cb(feedback):
    return

def service_cb(req):
    label = req.label
    resp = SendPositionResponse()
    goal = MoveBaseGoal()
    try:
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.pose.position.x = rosparam.get_param('/' + label +'/position/x')
        goal.target_pose.pose.position.y = rosparam.get_param('/' + label +'/position/y')
        goal.target_pose.pose.position.z = rosparam.get_param('/' + label +'/position/z')
        goal.target_pose.pose.orientation.x = rosparam.get_param('/' + label +'/orientation/x')
        goal.target_pose.pose.orientation.y = rosparam.get_param('/' + label +'/orientation/y')
        goal.target_pose.pose.orientation.z = rosparam.get_param('/' + label +'/orientation/z')
        goal.target_pose.pose.orientation.w = rosparam.get_param('/' + label +'/orientation/w')
        client.send_goal(goal, feedback_cb=feedback_cb)
        client.wait_for_result(rospy.Duration(100))
    except Exception as e:
        rospy.logerr(e.message)
    resp.success = "OK"
    return resp

service_name = '/send_pose_service'
goals_service = rospy.Service(service_name, SendPosition, service_cb)
rospy.loginfo(service_name + " service started.")
rospy.spin()