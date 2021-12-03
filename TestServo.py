import time
import dynamixel_edit
from jointdrive_edit import *
import math
import serialPorts

id = 15
null_position = math.pi * (5/6)
position = 0 #radiant, null position
position1 = -math.pi * (5/6) #max position
speed20 = 20 #rpm
speed60 = 60

#l = serialPorts.serialPortList()
#print(l)
#port = serial.Serial(port=str(l[0]), baudrate=1000000)

servo = JointDrive(id, ccw=False)

servo.setGoalPosSpeed(null_position, speed20, False)

time.sleep(3)

servo.setDesiredJointAngle(position, True)
servo.action()

time.sleep(3)

servo.setSpeedValue(speed20, False)
servo.setDesiredJointAngle(position, False)

time.sleep(3)

servo.setSpeedValue(speed60, False)
servo.setDesiredJointAngle(position1, False)

time.sleep(3)

angle = servo.getCurrentJointAngle()
print(f'Angle in rad: {angle}')

time.sleep(1)

speed = servo.getSpeedValue()
print(f'Speed in rpm(present): {speed}')


time.sleep(1)

temp = servo.getTemperature()
print(f'Temp in Cel.: {temp}')

servo.setDesiredJointAngle(null_position)
time.sleep(1)
servo.setDesiredJointAngle(position)
time.sleep(1)
servo.setDesiredJointAngle(position1)