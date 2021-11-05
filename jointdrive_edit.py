import math
from servo_ax12a_edit import *

# -do some factoring



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

    _ANGLE_UNIT = ServoAx12a._ANGLE_MAX_TICKS / ((ServoAx12a._ANGLE_MAX_DEGREE -
                                                  ServoAx12a._ANGLE_MIN_DEGREE) * math.pi * 2 / 360)     # Ticks per rad

    # Private methods    
    #----------------------------------------------------------------------
    # Constructor, defines the folowing variables: counterClockWise, angleOffset, angleMax, angleMin
    # id -> id of servo, cw -> rotating direction, aOffset -> angle offset,
    # aMax -> maximum angle allowed, aMin -> minimum angle allowed
    def __init__(self, id, ccw = False, aOffset = 0.0, aMax = math.pi * 2, aMin = -math.pi * 2):
        ### Implementierungsstart ###
        ### ID reicht erst einmal ###
        self.id = id
        self.aOffset = aOffset
        self.aMax = aMax
        self.aMin = aMin
        super().__init__(self.id) #dont know if i need this

        #when initialized
        # self.setDesiredJointAngle([150], True)
        # self.setSpeedValue()
        #...


    # Converts angle in radian to servo ticks
    # angle -> in radian, returns angle in servo ticks
    def __convertAngleToTicks(self, angle):
        ### Implementierungsstart ###
        return math.floor(angle * self._ANGLE_UNIT) #umrechnung ist falsch


    # Converts servo ticks to angle in radian
    # ticks -> servo ticks, returns angle in radian
    def __convertTicksToAngle(self, ticks):
        ### Implementierungsstart ###
        return ticks * (1/self._ANGLE_UNIT)

    # Converts speed in rpm to servo ticks
    # speed -> value in rpm
    def __convertSpeedToTicks(self, speed):
        return speed * (1/ServoAx12a._SPEED_UNIT)

    # Converts ticks to speed in rpm
    # ticks -> servo ticks
    def __convertTicksToSpeed(self, ticks):
        return ticks * ServoAx12a._SPEED_UNIT

    def __convertDegreeToRadian(self, degree):
        return degree * (math.pi/180)


    # Public methods    
    #----------------------------------------------------------------------
    # Get current angle of servo
    # returns angle in radian
    def getCurrentJointAngle(self):
        CurrentAngle = ServoAx12a.getPresentPosition()
        return self.__convertTicksToAngle(CurrentAngle)


    # Set servo to desired angle
    # angle -> in radian,
    def setDesiredJointAngle(self, angle, trigger = False):
        if angle > ServoAx12a._ANGLE_MAX_DEGREE or angle < ServoAx12a._ANGLE_MIN_DEGREE:
            return
        angle = self.__convertAngleToTicks(angle)
        ServoAx12a.setGoalPosition(self, angle, trigger) #convert angle(rad) to motor ticks

    # Set speed value of servo
    # speed -> angle speed in rpm
    def setSpeedValue(self, speed = 0, trigger=False):
        if speed > ServoAx12a._SPEED_MAX_RPM or speed < 0:
            return
        ServoAx12a.setMovingSpeed(self, self.__convertSpeedToTicks(speed), trigger) #convert speed(rpm) to motor ticks


    # Set servo to desired angle and speed
    # angle -> in radian,
    # speed -> speed of movement in rpm, speed = 0 -> maximum speed
    def setDesiredAngleSpeed(self, angle, speed = 0, trigger = False):
        self.setDesiredJointAngle(angle, trigger)
        self.setSpeedValue(speed, trigger)

