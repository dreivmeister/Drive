from serialPorts import *

# QUESTIONS:
#     -How to read/write words of data? For Bulk Read and Sync Write?
#     -do error handling
#     -do checksum control


# Classdefinition to implement dynamixel protocol
#===============================================================================
# Implements the dynamixel protocol 1.0
# ------------------------------------------------------------------------------
# Assigns the class object to a dedicated servo by the servo id
# Initializes the serial connection to the servo bus
# Handles the transfer of all required packet types with 1..n data bytes or -words
class Dynamixel:

    # Definition of protected class attributes
    # Accessible only within own and derived classes 
    #---------------------------------------------------------------------------
    _ID_BROADCAST = 0xFE

    # Definition of private class attributes, accessible only within own class
    #---------------------------------------------------------------------------
    # Define dynamixel constants
    __DYNAMIXEL_PORT_NR = 0                                                     # Index of dynamixel line in list
    __BAUDRATE = 1000000                                                        # Baudrate of dynamixel serial line
    __TIME_OUT_DEFAULT = 2                                                      # Default time out
    __DIRECT_ACTION = 3                                                         # Direct action command
    __TRIGGERT_ACTION = 4                                                       # Triggered action command
    __STATUS_PACKET_BASE_LENGTH = 6                                             # Base length of status packet
    __lines = serialPortList()                                                  # Contains all available serial lines
    __serial_port = serial.Serial(__lines[__DYNAMIXEL_PORT_NR],
                                  __BAUDRATE, timeout = __TIME_OUT_DEFAULT)   # Serial line object
    # Create templates of command packets 
    __pktAction = [255, 255, 0, 2, 5, 0]                                        # Packet to invoke action
    __pktReadData = [255, 255, 0, 4, 2, 0, 0, 0]                                # Packet to request date
    __pktWriteByte = [255, 255, 0, 4, 3, 0, 0, 0]                               # Packet to write byte
    __pktWriteNByte = [255, 255, 0, 0, 3, 0]                                    # Base-packet to write n-bytes
    __pktWriteWord = [255, 255, 0, 7, 3, 0, 0, 0, 0, 0, 0]                   # Packet to write word

    #---------------------------------------------------------------------------
    # Definition of private methods with implicit servo-id
    # Accessible only within own class
    #---------------------------------------------------------------------------
    # Constructor, sets id and defines error variable
    # id -> id of attached servo
    def __init__(self, id):
        self.id = id
        self.error = 0


    # Start predefined action on servo
    # execute the registered Reg Write instruction
    # id -> id of servo to ping, without id -> broadcast action
    def __doAction(self, id = _ID_BROADCAST):
        pktAction = self.__pktAction # copy base pkt

        pktAction[2] = id # place id

        pktAction[3] = 2

        pktAction[5] = 5

        pktAction[-1] = self.__checkSum(pktAction) # place checksum

        print(pktAction)
        self.__serial_port.write(bytearray(pktAction)) # sendCommand



    # Prepares and sends packet to servo in order to read data from servo memory
    # register -> register address of servo
    # nByte    -> number of bytes to read
    #__pktReadData = [255, 255, 0, 4, 2, 0, 0, 0]
    def __writeReadDataPkt(self, register, nByte):
        pktReadData = self.__pktReadData # copy base pkt

        pktReadData[2] = self.id # place id

        #base length 4 always

        pktReadData[5] = register  # place register address

        if nByte == 1:
            pktReadData[6] = 1 #length of data
        else:
            pktReadData[6] = 2 #length of data (bytes)


        pktReadData[7] = self.__checkSum(pktReadData) #calc check sum

        self.__serial_port.write(bytearray(pktReadData)) # sendCommand
        #print("SEND read: " + str(pktReadData))

        pktStatus = self.__doReadStatusPkt(self.__STATUS_PACKET_BASE_LENGTH + nByte)

        if nByte == 1:
            return pktStatus[-2] #data byte
        else:
            return pktStatus[-3:-1] #data bytes


    # Calculates check sum of packet list
    def __checkSum(self, pkt):
        s = sum(pkt[2:-1])
        return (~s) & 0xFF

    # Read status packet, set error value and get return values from servo
    # nByte -> number of bytes to read
    def __doReadStatusPkt(self, nByte):
        pktReadStatus = self.__serial_port.read(nByte) # read status packet of servo

        self.error = pktReadStatus[4] # set error value with error bit

        return pktReadStatus # return parameter values of status packet

    # Definition of protected methods
    # Accessible within own and derived classes
    #---------------------------------------------------------------------------
    # Read data byte from servo memory
    # register -> register address of servo
    # dtLen    -> number of data bytes to read
    #__pktReadData = [255, 255, 0, 4, 2, 0, 0, 0]
    def _requestNByte(self, register, dtLen = 1):
        return self.__writeReadDataPkt(register, dtLen)


    # Sends packet to servo in order to write n data bytes into servo memory
    # register -> register address of servo
    # data     -> list of bytes to write
    # trigger  -> False -> command is directly executed, True -> command is delayed until action command
    #__pktWriteNByte = [255, 255, 0, 0, 3, 0]
    def _writeNBytePkt(self, register, data, trigger):
        pktWriteNByte = Dynamixel.__pktWriteNByte
        pktWriteNByte[2] = self.id

        pktWriteNByte.extend([0]*3) #data byte(s) + register byte

        pktWriteNByte[3] = 5 #opcode-data low-data high- +2

        pktWriteNByte[5] = register # register address

        if trigger:
            pktWriteNByte[4] = 4 # REG WRITE

        #place bytes
        #start at index 6

        pktWriteNByte[6] = data & 255 #low byte
        pktWriteNByte[7] = data >> 8 #high byte

        pktWriteNByte[-1] = self.__checkSum(pktWriteNByte)

        self.__serial_port.write(bytearray(pktWriteNByte)) #write pkt to servo
        #print("SEND:" + str(pktWriteNByte))
        Dynamixel.__pktWriteNByte = [255, 255, 0, 0, 3, 0] #reset for some reason


    # Sends packet to servo in order to write data dword into servo memory
    # register -> register address of servo
    # data     -> list of words to write
    # trigger  -> False -> command is directly executed, True -> command is delayed until action command
    #__pktWriteWord = [255, 255, 0, 7, 3, 0, 0, 0, 0, 0, 0]
    #When Sync Writing to different registers
    def _writeNWordPkt(self, register, data, trigger):
        pktWriteWord = self.__pktWriteWord #copy base pkt
        pktWriteWord[2] = self.id #place id

        if trigger:
            pktWriteWord[4] = 4 #REG WRITE

        pktWriteWord[5] = register #place register address
        print(data[0], data[1])
        pktWriteWord[6] = data[0] & 255 #position low byte
        pktWriteWord[7] = data[0] >> 8 #position high byte

        pktWriteWord[8] = data[1] & 255 #speed low byte
        pktWriteWord[9] = data[1] >> 8 #speed high byte


        pktWriteWord[-1] = self.__checkSum(pktWriteWord) #place check sum
        print(pktWriteWord)
        self.__serial_port.write(pktWriteWord) #write pkt to servo


        # Read data word from servo memory
        # register -> register address of servo
        # dtWLen   -> number of data words to read
    def _requestNWord(self, register, dtWlen=1):
        pass


    # Definition of public methods with implicit servo-id
    # Accessible from everywere    
    #---------------------------------------------------------------------------
    # Show available serial lines
    def showSerialLines(self):
        print(Dynamixel.__lines)

    # Start predefined action on servo with assigned id
    def action(self):
        return self.__doAction()

    # Get last error    
    def getLastError(self):
        return self.error

