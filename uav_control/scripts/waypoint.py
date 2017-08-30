#!/usr/bin/env python

import rospy
import mavros
import sensor_msgs
import yaml
#from mavros.msg import *
from mavros_msgs.msg import *
from mavros_msgs.srv import *
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix

#global variables
latitude = 0.0
longitude = 0.0
altitude = 0.0

def waypoint_callback(data):
	print("\n----------\nwaypoint_callback")
	rospy.loginfo("Got waypoint: %s", data)
	#print(len(data.waypoints))
	rospy.loginfo("is_current: %s", data.waypoints[1].is_current)
	print(data)


def globalPosition_callback(data):
	#print("\n----------\nglobalPosition_callback")
	global latitude
	global longitude
	global altitude
	latitude = data.latitude
	longitude = data.longitude
	altitude = data.altitude


def main():
	rospy.init_node('wayPoint')
	rospy.Subscriber("/mavros/mission/waypoints", WaypointList, waypoint_callback)
	rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, globalPosition_callback)
	global latitude
	global longitude

	#Clearing waypoints
	print("\n----------CLEARING----------")
	rospy.wait_for_service("/mavros/mission/clear")
	print("Clearing Waypoints!!!")
	waypoint_clear = rospy.ServiceProxy("/mavros/mission/clear", WaypointClear)
	resp = waypoint_clear()
	print(resp)
	rospy.sleep(5)

	#Call waypoints_pull
	print("\n----------PULLING----------")
	rospy.wait_for_service("/mavros/mission/pull")
	print("Calling Waypoint_pull Service")
	waypoint_pull = rospy.ServiceProxy("/mavros/mission/pull", WaypointPull)
	resp = waypoint_pull()
	print(resp)
	rospy.sleep(5)
	

	#Arming
	print("\n----------ARMING----------")
	rospy.wait_for_service("/mavros/cmd/arming")
	print("Arming UAV!!!")
	uav_arm = rospy.ServiceProxy("/mavros/cmd/arming", CommandBool)
	resp = uav_arm(1)
	print(resp)
	rospy.sleep(5)
	
	#Switching Modes
	#print("\nSwitching to AUTO mode")
	#rospy.wait_for_service("/mavros/set_mode")
	#print("Switching to AUTO mode, same as mission!!!")
	#uav_mode_switch = rospy.ServiceProxy("/mavros/set_mode", SetMode)
	#resp = uav_mode_switch(220)
	#print(resp)
	#rospy.sleep(5)
	
	#Takeoff
	#print("\nTakeoff")
	#rospy.wait_for_service("/mavros/cmd/takeoff")
	#print("Takeoff UAV!!!")
	#uav_takeoff = rospy.ServiceProxy("/mavros/cmd/takeoff", CommandTOL)
	#resp = uav_takeoff()
	#print(resp)
	#rospy.sleep(5)
	
	#Sending waypoints_push
	print("\n----------PUSHING----------")
	print("Waiting for MAVROS service...")
	rospy.wait_for_service("/mavros/mission/push")
	
	waypoints = [
		Waypoint(frame = 3, command = 22, is_current = True, autocontinue = True, param1 = 5, x_lat = 47.3975922, y_long = 8.5455939, z_alt = 5),
		Waypoint(frame = 3, command = 16, is_current = False, autocontinue = True, param1 = 5, x_lat = 47.3979922, y_long = 8.5455939, z_alt = 10),
		Waypoint(frame = 3, command = 21, is_current = False, autocontinue = True, param1 = 5, x_lat = 47.3989922, y_long = 8.5455939, z_alt = 15)
	]
	
	waypoint_push = rospy.ServiceProxy("/mavros/mission/push", WaypointPush)
	resp = waypoint_push(waypoints)
	print(resp)
	#print(waypoints)
	rospy.sleep(5)
	
	#Call waypoints_pull
	print("\n----------PULLING----------")
	rospy.wait_for_service("/mavros/mission/pull")
	print("Calling Waypoint_pull Service")
	waypoint_pull = rospy.ServiceProxy("/mavros/mission/pull", WaypointPull)
	resp = waypoint_pull()
	print(resp)
	rospy.sleep(5)
	
	while True:
		print(" lat " + repr(latitude) + " long " + repr(longitude) + " alt " + repr(altitude))
		rospy.sleep(2)
		latlongalt = (latitude-47.39899)+(longitude-8.54559)+(altitude-488)
		if latlongalt<0.0001:
			rospy.wait_for_service("/mavros/mission/push")
			resp = waypoint_push(waypoints)
			waypoints = [
				Waypoint(frame = 3, command = 22, is_current = True, autocontinue = True, param1 = 5, x_lat = 47.3975922, y_long = 8.5455939, z_alt = 20),
			]
			resp = waypoint_push(waypoints)
			print(resp)
			rospy.sleep(5)
			break

			print("fin")
			rospy.spin()

	


if __name__ == '__main__':
	main()

