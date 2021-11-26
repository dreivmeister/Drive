import math
from servo_ax12a_edit import *


# Class definition of ax12a-controller class, defines interface to the robot
#===============================================================================
# Implements the interface between leg- and servo class
# ------------------------------------------------------------------------------
# Provides all required methods that allow the leg class to control the servo
# Implements all nessesary codomain conversion between leg- and servo values
# Limits values too valid servo values
# Servo uses ticks from 0 to 1023 for angle and speed
# Leg uses angles in radian and rotation per minit for speed
# Defines zero angle as average of min- and max value -> positive and negativ angles are allowed


class JointDrive(ServoAx12a):

    # Definition of public class attributes
    #----------------------------------------------------------------------
    _ANGLE_RADIAN_ZERO = (ServoAx12a._ANGLE_MAX_DEGREE - ServoAx12a._ANGLE_MIN_DEGREE) * math.pi / 360
    # Zero angle offset of servo in radian

    # _ANGLE_UNIT = ServoAx12a._ANGLE_MAX_TICKS / ((ServoAx12a._ANGLE_MAX_DEGREE -
    #                                               ServoAx12a._ANGLE_MIN_DEGREE) * math.pi * 2 / 360)     # Ticks per rad

    _ANGLE_UNIT = ServoAx12a._ANGLE_MAX_TICKS / ServoAx12a._ANGLE_MAX_RAD

    # Private methods    
    #----------------------------------------------------------------------
    # Constructor, defines the folowing variables: counterClockWise, angleOffset, angleMax, angleMin
    # id -> id of servo, cw -> rotating direction, aOffset -> angle offset,
    # aMax -> maximum angle allowed, aMin -> minimum angle allowed
    def __init__(self, id, ccw = False, aOffset = 0.0, aMax = (5/3)*math.pi, aMin = 0):
        ### Implementierungsstart ###
        ### ID reicht erst einmal ###
        self.id = id
        self.ccw = ccw
        self.aOffset = aOffset
        self.aMax = aMax
        self.aMin = aMin
        #super().__init__(self.id) #dont know if i need this


    # Converts angle in radian to servo ticks
    # angle -> in radian, returns angle in servo ticks
    #lauft
    def __convertAngleToTicks(self, angle):
        return math.floor(angle * self._ANGLE_UNIT)

    # Converts servo ticks to angle in radian
    # ticks -> servo ticks, returns angle in radian
    #lauft
    def __convertTicksToAngle(self, ticks):
        return ticks * (1/self._ANGLE_UNIT)

    # Converts speed in rpm to servo ticks
    # speed -> value in rpm
    def __convertSpeedToTicks(self, speed):
        return math.floor(speed * ServoAx12a._SPEED_UNIT)

    # Converts ticks to speed in rpm
    # ticks -> servo ticks
    def __convertTicksToSpeed(self, ticks):
        return ticks * (1/ServoAx12a._SPEED_UNIT)



    # Public methods    
    #----------------------------------------------------------------------
    # Get current angle of servo
    # returns angle in radian
    def getCurrentJointAngle(self):
        CurrentAngle = ServoAx12a.getPresentPosition(self)

        if len(CurrentAngle) == 1:
            word = CurrentAngle[0]
        else:
            word = ((CurrentAngle[1] << 8) | CurrentAngle[0]) #put high byte and low byte together and convert to decimal

        return self.__convertTicksToAngle(word) #return decimal ticks to angle in radian

    def getPresentTemperature(self):
        return ServoAx12a.getTemperature()

    # Set servo to desired angle
    # angle -> in radian,
    def setDesiredJointAngle(self, angle, trigger = False):
        if not self.ccw:
             angle = (5/6 * math.pi) + angle + self.aOffset
        else:
             angle = (5/6 * math.pi) - angle + self.aOffset

        if angle > self.aMax or angle < self.aMin: #check for allowed position
            return

        angle = self.__convertAngleToTicks(angle) #convert angle(rad) to motor ticks
        ServoAx12a.setGoalPosition(self, angle, trigger)

    # Set speed value of servo
    # speed -> angle speed in rpm
    def setSpeedValue(self, speed = 0, trigger=False):
        if speed > ServoAx12a._SPEED_MAX_RPM or speed < 0:
            return

        speed = self.__convertSpeedToTicks(speed)

        ServoAx12a.setMovingSpeed(self, speed, trigger) #convert speed(rpm) to motor ticks

    def getSpeedValue(self):
        CurrentSpeed = ServoAx12a.getPresentSpeed(self)

        if len(CurrentSpeed) == 1:
            word = CurrentSpeed[0]
        else:
            word = ((CurrentSpeed[1] << 8) | CurrentSpeed[0])  # put high byte and low byte together and convert to decimal

        return self.__convertTicksToSpeed(word)  # return decimal ticks to angle in radian

    # Set servo to desired angle and speed
    # angle -> in radian,
    # speed -> speed of movement in rpm, speed = 0 -> maximum speed
    def setDesiredAngleSpeed(self, angle, speed = 0, trigger = False):
        self.setDesiredJointAngle(angle, trigger)
        self.setSpeedValue(speed, trigger)

    # Set goal position and speed
    # position: 0 to 1023 is available. The unit is 0.29 degree.
    # speed:    0~1023 can be used, and the unit is about 0.111rpm.
    #           If it is set to 0, it means the maximum rpm of the motor is used without controlling the speed.
    #           If it is 1023, it is about 114rpm.
    def setGoalPosSpeed(self, angle, speed, trigger = False):
        if angle > ServoAx12a._ANGLE_MAX_RAD or angle < ServoAx12a._ANGLE_MIN_RAD:  # check for allowed position
            return

        angle = self.__convertAngleToTicks(angle)  # convert angle(rad) to motor ticks
        ServoAx12a.setGoalPosition(self, angle, trigger)

        if speed > ServoAx12a._SPEED_MAX_RPM or speed < 0:
            return

        speed = self.__convertSpeedToTicks(speed)
        ServoAx12a.setMovingSpeed(self, speed, trigger)

