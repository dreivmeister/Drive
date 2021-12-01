import time
from jointdrive_edit import *
import math

id = 15
position =  math.pi * (5/6) #radiant, null position
position1 = math.pi * (5/3) #max position
speed20 = 20 #rpm
speed60 = 60


Dynamixel.showSerialLines()

servo = JointDrive(id, ccw=False)



servo.setSpeedValue(speed20, False)
servo.setDesiredJointAngle(position, False)

time.sleep(1)

servo.setSpeedValue(speed60, False)
servo.setDesiredJointAngle(position1, False)

time.sleep(1)

angle = servo.getCurrentJointAngle()
print(f'Angle in rad: {angle}')

time.sleep(1)

speed = servo.getSpeedValue()
print(f'Speed in rpm(present): {speed}')

time.sleep(1)

temp = servo.getTemperature()
print(f'Temp in Cel.: {temp}')
