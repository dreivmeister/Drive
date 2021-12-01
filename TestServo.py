import time
import serialPorts
from jointdrive_edit import *
import math

id = 15
position =  math.pi * (5/6) #radiant

Dynamixel.showSerialLines()

servo = JointDrive(id, ccw=True)

servo.setDesiredJointAngle(position, True)
Dynamixel.action()


# servo.setDesiredJointAngle(position, False)
#
# time.sleep(1)
#
# angle = servo.getCurrentJointAngle()
# print(f'Angle in rad: {angle}')
#
#
# speed = servo.getSpeedValue()
# print(f'Speed in rpm: {speed}')

temp = servo.getTemperature()
print(f'Temp in Cel.: {temp}')
