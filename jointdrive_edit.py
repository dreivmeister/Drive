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
    _ANGLE_RADIAN_ZERO = (ServoAx12a._ANGLE_MAX_DEGREE - ServoAx12a._ANGLE_MIN_DEGREE) * math.pi / 360 #5/6*pi
    # Zero angle offset of servo in radian

    # _ANGLE_UNIT = ServoAx12a._ANGLE_MAX_TICKS / ((ServoAx12a._ANGLE_MAX_DEGREE -
    #                                               ServoAx12a._ANGLE_MIN_DEGREE) * math.pi * 2 / 360)     # Ticks per rad

    _ANGLE_UNIT = ServoAx12a._ANGLE_MAX_TICKS / ServoAx12a._ANGLE_MAX_RAD

    # Private methods    
    #----------------------------------------------------------------------
    # Constructor, defines the folowing variables: counterClockWise, angleOffset, angleMax, angleMin
    # id -> id of servo, cw -> rotating direction, aOffset -> angle offset,
    # aMax -> maximum angle allowed, aMin -> minimum angle allowed
    def __init__(self, id, ccw=False, aOffset=0.0, aMax=math.radians(150), aMin=-math.radians(150), prt=False):
        ### Implementierungsstart ###
        ### ID reicht erst einmal ###
        super().__init__(id, prt)
        self.id = id
        self.ccw = ccw
        self.aOffset = aOffset
        self.aMax = aMax
        self.aMin = aMin
        self.prt = prt


    # Converts angle in radian to servo ticks
    # angle -> in radian, returns angle in servo ticks
    def __convertAngleToTicks(self, angle):
        return math.floor(angle * self._ANGLE_UNIT)

    # Converts servo ticks to angle in radian
    # ticks -> servo ticks, returns angle in radian
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
            word = CurrentAngle[0] #single data byte
        else:
            word = ((CurrentAngle[1] << 8) | CurrentAngle[0]) #put high byte and low byte together and convert to decimal

        angle = self.__convertTicksToAngle(word) #convert ticks to angle in radian and return

        if not self.ccw:
            angle = angle - self._ANGLE_RADIAN_ZERO - self.aOffset
        else:
            angle = self._ANGLE_RADIAN_ZERO + self.aOffset - angle

        return angle

    def getPresentTemperature(self):
        return ServoAx12a.getTemperature()

    # Set servo to desired angle
    # angle -> in radian,
    def setDesiredJointAngle(self, angle, trigger = False):
        for i in range(0, len(angle)):

            if angle[i] > self.aMax or angle[i] < self.aMin: #check for allowed position
                return

            if not self.ccw:
                angle[i] = self._ANGLE_RADIAN_ZERO + angle[i] + self.aOffset #clockwise
            else:
                angle[i] = self._ANGLE_RADIAN_ZERO - angle[i] + self.aOffset #counterclockwise

            angle[i] = self.__convertAngleToTicks(angle[i]) #convert angle(rad) to motor ticks
            print(angle[i])
        ServoAx12a.setGoalPosition(self, angle, trigger)

    # Set speed value of servo
    # speed -> angle speed in rpm
    def setSpeedValue(self, speed = 0, trigger=False):
        if speed[0] > ServoAx12a._SPEED_MAX_RPM or speed[0] < 0:
            return

        speed[0] = self.__convertSpeedToTicks(speed[0])

        ServoAx12a.setMovingSpeed(self, speed, trigger) #convert speed(rpm) to motor ticks

    def getSpeedValue(self):
        CurrentSpeed = ServoAx12a.getPresentSpeed(self)

        if len(CurrentSpeed) == 1:
            word = CurrentSpeed[0]
        else:
            word = ((CurrentSpeed[1] << 8) | CurrentSpeed[0])  # put high byte and low byte together and convert to decimal

        return self.__convertTicksToSpeed(word)  #convert ticks to speed(rpm) and return

    #untested
    # Set goal position and speed
    # position: 0 to 1023 is available. The unit is 0.29 degree.
    # speed:    0~1023 can be used, and the unit is about 0.111rpm.
    #           If it is set to 0, it means the maximum rpm of the motor is used without controlling the speed.
    #           If it is 1023, it is about 114rpm.
    # data = [angle, speed]
    def setGoalPosSpeed(self, data, trigger = False):
        if data[0] > self.aMax or data[0] < self.aMin:  # check for allowed position
            return


        if not self.ccw:
            data[0] = self._ANGLE_RADIAN_ZERO + data[0] + self.aOffset  # clockwise
        else:
            data[0] = self._ANGLE_RADIAN_ZERO - data[0] + self.aOffset  # counterclockwise

        data[0] = self.__convertAngleToTicks(data[0])  # convert angle(rad) to motor ticks

        if  data[1] > ServoAx12a._SPEED_MAX_RPM or data[1] < 0:
            return

        data[1] = self.__convertSpeedToTicks(data[1])

        ServoAx12a.setGoalPositionMovingSpeed(self, data, trigger)





