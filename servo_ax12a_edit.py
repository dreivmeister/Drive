import math

from dynamixel_edit import *

# TO-Do:
#     -Might have to do unit conversions
#     -Look at Angle/Speed Limits of servo
#     -Look at Rotation Direction


# Definition of Servo-Ax12a-controller class, defines control and status methods
#===============================================================================
# Implements communication commands to servo AX12A
# ------------------------------------------------------------------------------
# Uses the commands of Dynamixel class to send and receive the required servo values
class ServoAx12a(Dynamixel):

    # Definition of private class attributes
    #----------------------------------------------------------------------
    # EEPROM communication registers addresses
    __RETURN_DELAY_TIME = 0x05                                                  # time of return delay (n * 2 in [uS]), 1 byte, read/write	
    __RETURN_LEVEL = 0x10                                                       # status return level, 1 byte, read/write
    # RAM communication registers addresses
    __GOAL_POSITION = 0x1E                                                      # goal position, 2 byte, read/write
    __MOVING_SPEED = 0x20                                                       # moving speed, 2 byte, read/write
    __PRESENT_POSITION = 0x24                                                   # current position, 2 byte, read only
    __PRESENT_SPEED = 0x26                                                      # current speed, 2 byte, read only	

    # Definition of protected class attributes
    #----------------------------------------------------------------------
    # Servo constants
    _ANGLE_MAX_TICKS = 1023                                                     # ticks at highest position (330 degree)
    _ANGLE_MIN_TICKS = 0                                                        # ticks at lowest position (30 degree)
    _ANGLE_MAX_DEGREE = 300                                                     # highest angle reachable is 330 degree
    _ANGLE_MIN_DEGREE = 0                                                       # lowest angle reachable is 30 degree
    _ANGLE_MAX_RAD = (5/3)*math.pi                                                      # highest rad reachable (300 deg)
    _ANGLE_MIN_RAD = 0                                                          # lowest rad reachable
    _ANGLE_UNIT = 0.29                                                          # 0.29 degree per tick
    _SPEED_UNIT = (1023/113.5)                                                         # 0.111 rpm per tick
    _SPEED_MAX_TICKS = 1023                                                     # 1023 
    _SPEED_MAX_RPM = 1023 * 0.111                                               # 1023 * 0.111 = 113.5 rpm

    # Definition of public class attributes
    #----------------------------------------------------------------------
    # Definition of valid return levels
    RETURN_LEVEL_PING_COMMAND = 0                                               # Status packet is only returned for ping
    RETURN_LEVEL_READ_COMMANDS = 1                                              # Status packet is returned for ping and read requests
    RETURN_LEVEL_ALL_COMMANDS = 2                                               # Status packet is returned for ping, read requests and writes
    # Defines the wait time the servo switches from receive to send mode
    # when a read request packet was received                                             
    RETURN_DELAY_VALUE = 10                                                     # Definition of return delay time, value * 2 -> [uS]

    # Definition of private methods
    #----------------------------------------------------------------------
    # Constructor, return level and return delay are set
    def __init__(self, id):
        ### Implementierungsstart ###
        self.id = id
        super().__init__(self.id)



    # Getter methods for servo Ax12a
    #----------------------------------------------------------------------
    # Get time of return delay
    # returns: 0 to 254 (0xFE) can be used, and the delay time per data value is 2 usec.
    def getReturnDelay(self):
        return self.__RETURN_DELAY_TIME

    # Get status return level
    # returns: 0->No return against all commands (Except PING Command), 1->Return only for the READ command, 2->Return for all commands
    def getReturnLevel(self):
        return self.__RETURN_LEVEL

    # Get goal position
    # returns: value of 0 to 1023, the unit is 0.29 degree.
    def getGoalPosition(self):
        GoalPosition = Dynamixel._requestNByte(self, self.__GOAL_POSITION, 2) #has to return something
        return GoalPosition * self._ANGLE_UNIT

    # Get moving speed
    # returns: 0 to 1023, the unit is about 0.111rpm.
    #          If it is set to 0, it means the maximum rpm of the motor is used without controlling the speed.
    #          If it is 1023, it is about 114rpm.
    def getMovingSpeed(self):
        MovingSpeed = Dynamixel._requestNByte(self, self.__MOVING_SPEED, 2)
        return MovingSpeed * self._SPEED_UNIT

    # Get present position
    # returns: value of 0 to 1023, the unit is 0.29 degree.
    def getPresentPosition(self):
        return Dynamixel._requestNByte(self, self.__PRESENT_POSITION, 2)

    # Get present speeed
    # returns: 0 to 1023, the unit is about 0.111rpm.
    #          If it is set to 0, it means the maximum rpm of the motor is used without controlling the speed.
    #          If it is 1023, it is about 114rpm.
    def getPresentSpeed(self):
        PresentSpeed = Dynamixel._requestNByte(self, self.__PRESENT_SPEED, 2)
        return PresentSpeed * self._SPEED_UNIT

    # Get Goal position and speed, returns: [position, speed]
    # position: 0 ~ 1023, 
    # speed:    0 to 1023, the unit is about 0.111rpm.
    #           If it is 0, it means the maximum rpm of the motor is used without controlling the speed.
    #           If it is 1023, it is about 114rpm.
    def getGoalPosSpeed(self):
        return [self.getGoalPosition(), self.getPresentSpeed()]

    # Get present position and speed, returns: [position, speed]
    # position: 0 ~ 1023, 
    # speed:    0 to 1023, the unit is about 0.111rpm.
    #           If it 0, it means the maximum rpm of the motor is used without controlling the speed.
    #           If it is 1023, it is about 114rpm.
    def getPresPosSpeed(self):
        return [self.getPresentPosition(), self.getPresentSpeed()]


    # Setter methods for servo Ax12a
    #----------------------------------------------------------------------
    # Set time of return delay
    # delay: 0 to 254 (0xFE) can be used, and the delay time per data value is 2 usec.
    def setReturnDelay(self, delay, trigger = False):
        self.__RETURN_DELAY_TIME = delay
        Dynamixel._writeNBytePkt(self, self.__RETURN_DELAY_TIME, [delay], trigger)

    # Set status return level
    # 0->No return against all commands (Except PING Command), 1->Return only for the READ command, 2->Return for all commands
    def setReturnLevel(self, level, trigger = False):
        self.__RETURN_LEVEL = level
        Dynamixel._writeNBytePkt(self, self.__RETURN_LEVEL, [level], trigger)



    # Set goal position
    # position: motor ticks
    def setGoalPosition(self, position, trigger = False):
        Dynamixel._writeNBytePkt(self, self.__GOAL_POSITION, position, trigger)

    # Set moving speed
    # speed: 0~1023 can be used, and the unit is about 0.111rpm.
    #        If it is set to 0, it means the maximum rpm of the motor is used without controlling the speed.
    #        If it is 1023, it is about 114rpm.
    def setMovingSpeed(self, speed, trigger = False):
        Dynamixel._writeNBytePkt(self, self.__MOVING_SPEED, speed, trigger)

    # Set goal position and speed
    # position: 0 to 1023 is available. The unit is 0.29 degree.
    # speed:    0~1023 can be used, and the unit is about 0.111rpm.
    #           If it is set to 0, it means the maximum rpm of the motor is used without controlling the speed.
    #           If it is 1023, it is about 114rpm.
    def setGoalPosSpeed(self, position, speed, trigger = False):
        self.setGoalPosition(position, trigger)
        self.setMovingSpeed(speed, trigger)
        
