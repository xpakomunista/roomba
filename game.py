#
# game.py
#
# Simple tester for the Roomba Interface
# from create.py
#
# Adjust your ROOMBA_PORT if necessary.
# python game.py 
# starts a pygame window from which the 
# Roomba can be controlled with w/a/s/d.
# Use this file to play with the sensors.

import pygame
import create
import time

ROOMBA_PORT = "/dev/tty.usbserial-DA017V6X"
# Change the roomba port to whatever is on your
# machine. On a Mac it's something like this.
# On Linux it's usually tty.USB0 and on Win
# its to serial port.

robot = create.Create(ROOMBA_PORT)
robot.toSafeMode()
#robot.printSensors()

pygame.init()
size = width, height = 320, 240
pygame.display.set_mode(size)

MAX_FORWARD = 500
MAX_ROTATION = 2000
robot_dir = 0
robot_rot = 0

wall_fun = robot.senseFunc(create.WALL_SIGNAL)
wall_ir = robot.senseFunc(create.WALL_IR_SENSOR)
angle_fun = robot.senseFunc(create.ANGLE)

lb_left = robot.senseFunc(create.LIGHTBUMP_LEFT)
lb_front_left = robot.senseFunc(create.LIGHTBUMP_FRONT_LEFT)
lb_center_left = robot.senseFunc(create.LIGHTBUMP_CENTER_LEFT)
lb_center_right = robot.senseFunc(create.LIGHTBUMP_CENTER_RIGHT)
lb_front_right = robot.senseFunc(create.LIGHTBUMP_FRONT_RIGHT)
lb_right = robot.senseFunc(create.LIGHTBUMP_RIGHT)
#dist_fun = robot.senseFunc(create.DISTANCE)

robot.resetPose()

while True:
	senses = robot.sensors([create.WALL_SIGNAL, create.WALL_IR_SENSOR, create.LEFT_BUMP, create.RIGHT_BUMP, create.POSE])
	x,y,th = robot.getPose()	
	print ("{} {} {} {} {} {}".format(lb_left(), lb_front_left(), lb_center_left(), lb_center_right(), lb_front_right(), lb_right()) )
	#print ("wall {}, wall_ir {}".format(wall_fun(), wall_ir()))
	# if wall_ir() >0:
	# 	print ("Wall in {}".format(wall_fun()))
	update_roomba = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			robot.go(0,0)
			robot.close()
			pygame.quit(); #sys.exit() if sys is imported
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				robot_dir+=MAX_FORWARD
				update_roomba = True
			if event.key == pygame.K_s:
				robot_dir-=MAX_FORWARD
				update_roomba = True
			if event.key == pygame.K_a:
				robot_rot+=MAX_ROTATION
				update_roomba = True
			if event.key == pygame.K_d:
				robot_rot-=MAX_ROTATION
				update_roomba = True
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
			if event.key == pygame.K_SPACE:
				print("Angle: {}".format(angle_fun()))			
				robot.resetPose()
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w:
				robot_dir-=MAX_FORWARD
				update_roomba = True
			if event.key == pygame.K_s:
				robot_dir+=MAX_FORWARD
				update_roomba = True
			if event.key == pygame.K_a:
				robot_rot-=MAX_ROTATION
				update_roomba = True
			if event.key == pygame.K_d:
				robot_rot+=MAX_ROTATION
				update_roomba = True

	if update_roomba == True:		
		robot.go(robot_dir,robot_rot)
		time.sleep(0.2)
		
