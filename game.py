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
import os
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
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Roomba Test')

img_roomba_top = pygame.image.load(os.path.join('img', 'roomba.png'))

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

# Display some text
#font = pygame.font.Font(None, 18)
font = pygame.font.SysFont("calibri",16)

# Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()


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
	senses = robot.sensors([create.WALL_SIGNAL, create.WALL_IR_SENSOR, create.LEFT_BUMP, create.RIGHT_BUMP, create.POSE, create.ENCODER_LEFT, create.ENCODER_RIGHT, create.CLIFF_LEFT_SIGNAL, create.CLIFF_FRONT_LEFT_SIGNAL, create.CLIFF_FRONT_RIGHT_SIGNAL, create.CLIFF_RIGHT_SIGNAL])
	
	
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

	# done with the actual roomba stuff
	# now print.

	screen.blit(background, (0, 0))
	screen.blit(img_roomba_top, (0,0))
	#Light Bump
	screen.blit(font.render("{}".format(lb_left()), 1, (10, 10, 10)), (112, 136))
	screen.blit(font.render("{}".format(lb_front_left()), 1, (10, 10, 10)), (159, 62))
	screen.blit(font.render("{}".format(lb_center_left()), 1, (10, 10, 10)), (228, 19))

	screen.blit(font.render("{}".format(lb_center_right()), 1, (10, 10, 10)), (457, 19))
	screen.blit(font.render("{}".format(lb_front_right()), 1, (10, 10, 10)), (484, 54))
	screen.blit(font.render("{}".format(lb_right()), 1, (10, 10, 10)), (469, 115))
	#Wall Sensors
	screen.blit(font.render("{}".format(senses[create.WALL_IR_SENSOR]), 1, (10, 10, 10)), (376, 396))
	screen.blit(font.render("{}".format(senses[create.WALL_SIGNAL]), 1, (10, 10, 10)), (376, 416))
	#Bumpers
	screen.blit(font.render("{}".format(senses[create.LEFT_BUMP]), 1, (10, 10, 10)), (142, 396))
	screen.blit(font.render("{}".format(senses[create.RIGHT_BUMP]), 1, (10, 10, 10)), (142, 416))
	#Encoders
	screen.blit(font.render("{}".format(senses[create.ENCODER_LEFT]), 1, (10, 10, 10)), (635, 396))
	screen.blit(font.render("{}".format(senses[create.ENCODER_RIGHT]), 1, (10, 10, 10)), (635, 416))
	#Cliff Sensors
	screen.blit(font.render("{}".format(senses[create.CLIFF_LEFT_SIGNAL]), 1, (10, 10, 10)), (635, 16))
	screen.blit(font.render("{}".format(senses[create.CLIFF_FRONT_LEFT_SIGNAL]), 1, (10, 10, 10)), (635, 35))
	screen.blit(font.render("{}".format(senses[create.CLIFF_FRONT_RIGHT_SIGNAL]), 1, (10, 10, 10)), (635, 54))
	screen.blit(font.render("{}".format(senses[create.CLIFF_RIGHT_SIGNAL]), 1, (10, 10, 10)), (635, 73))


	pygame.display.flip()
		
