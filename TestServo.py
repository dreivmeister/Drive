import time
import serialPorts
from jointdrive_edit import *
import math


# create serial port connection
#l = serialPorts.serialPortList()
#print(l)
#port = serial.Serial(port=str(l[0]), baudrate=1000000)



# #auxiliary methods
# def calcCheckSum(pkt):
#     s = sum(pkt[2:-1])                              # add all values from servo-id to last parameter
#     return (~s) & 0xFF                              # invert sum bit-wise and limit to byte range
#
# def sendCommand(command):
#     command[-1] = calcCheckSum(command)             # calculate check sum and store it into last command entry
#     port.write(bytearray(command))                  # send command to serial line
#     print("send:", command)


# # main programm
# servoId = 4                                      # Id of Servo
#
# command = [255, 255, servoId, 5, 4, 30, 0, 0, 0]    # command list
#
# # Set to position 300
# position = 10                                      # define position
# command[6] = position & 255                         # set data low byte in command list
# command[7] = position >> 8                          # set data high byte in command list
# sendCommand(command)
# time.sleep(1)


id = 4
position = - math.pi * (5/6) #radiant
servo = JointDrive(id, ccw=True)

servo.setDesiredJointAngle(position, False)


time.sleep(1)

angle = servo.getCurrentJointAngle()
print(f'Angle in rad: {angle}')


speed = servo.getSpeedValue()
print(f'Speed in rpm: {speed}')

temp = servo.getTemperature()
print(f'Temp in Cel.: {temp}')
