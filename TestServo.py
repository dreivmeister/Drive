import time
import dynamixel_edit
from jointdrive_edit import *
import math
import serialPorts

id = 15
mid_pos = 0
max_pos = (5/6)*math.pi
min_pos = -(5/6)*math.pi
speed20 = 20 #rpm
speed60 = 60

#l = serialPorts.serialPortList()
#print(l)
#port = serial.Serial(port=str(l[0]), baudrate=1000000)

servo = JointDrive(id, ccw=False)

servo.setDesiredJointAngle(mid_pos)
time.sleep(2)
servo.setDesiredJointAngle(min_pos)
time.sleep(2)
servo.setDesiredJointAngle(max_pos)


servo.setGoalPosSpeed(min_pos, speed20, False)

time.sleep(3)

servo.setDesiredJointAngle(mid_pos, True)
servo.action()

time.sleep(3)

angle = servo.getCurrentJointAngle()
print(f'Angle in rad: {angle}')

time.sleep(1)

speed = servo.getSpeedValue()
print(f'Speed in rpm(present): {speed}')

time.sleep(1)

temp = servo.getTemperature()
print(f'Temp in Cel.: {temp}')
