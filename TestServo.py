import time
import math
from jointdrive_edit import *

id = 4
mid_pos = [0]
max_pos = [(5/6)*math.pi]
min_pos = [-(5/6)*math.pi]
speed20 = [20]
speed60 = [60]


servo = JointDrive(id, ccw=False, prt=True, aMax=math.radians(120), aMin=math.radians(-120))


servo.setDesiredJointAngle([math.radians(100)])
time.sleep(2)
print(servo.getCurrentJointAngle())


servo.setGoalPosSpeed([math.radians(90), 60])
time.sleep(2)
print(servo.getCurrentJointAngle())
print(servo.getSpeedValue())
