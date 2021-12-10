from serialPorts import *
import copy
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
    __DYNAMIXEL_PORT_NR = 1                                                     # Index of dynamixel line in list
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
    __pktWriteNByte = [255, 255, 0, 0, 3, 0, 0]                                 # Base-packet to write n-bytes
    __pktWriteWord = [255, 255, 0, 7, 3, 0, 0]                                  # Packet to write word

    #---------------------------------------------------------------------------
    # Definition of private methods with implicit servo-id
    # Accessible only within own class
    #---------------------------------------------------------------------------
    # Constructor, sets id and defines error variable
    # id -> id of attached servo
    def __init__(self, id, prt):
        self.id = id
        self.error = 0
        self.prt = prt


    # Start predefined action on servo
    # execute the registered Reg Write instruction
    # id -> id of servo to ping, without id -> broadcast action
    def __doAction(self, id = _ID_BROADCAST):
        pktAction = copy.deepcopy(self.__pktAction) # copy base pkt

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
        pktReadData = copy.deepcopy(self.__pktReadData) # copy base pkt

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
        print(len(pktReadStatus))
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
    #__pktWriteNByte = [255, 255, 0, 0, 3, 0, 0]
    # e.g. data = [200,300,1020]
    def _writeNBytePkt(self, register, data, trigger):
        nBytes = len(data)
        pktWriteNByte = copy.deepcopy(self.__pktWriteNByte)
        pktWriteNByte[2] = self.id

        pktWriteNByte.extend([0]*nBytes) #data byte(s) + register byte

        pktWriteNByte[3] = nBytes+3 #data bytes + register + 2

        #REG WRITE
        if trigger:
            pktWriteNByte[4] = 4

        pktWriteNByte[5] = register # register address

        i = 6
        for date in data:
            pktWriteNByte[i] = date
            i += 1

        pktWriteNByte[-1] = self.__checkSum(pktWriteNByte)

        self.__serial_port.write(bytearray(pktWriteNByte)) #write pkt to servo
        #print("SEND:" + str(pktWriteNByte))


    def _writeNWordPkt(self, register, data, trigger):
        nBytes = len(data)*2
        #print(data)
        pktWriteNWord = copy.deepcopy(self.__pktWriteWord) #copy base pkt
        pktWriteNWord[2] = self.id

        pktWriteNWord.extend([0]*nBytes) #data byte(s) + register byte

        pktWriteNWord[3] = nBytes+3 #data bytes + register + 2

        #REG WRITE
        if trigger:
            pktWriteNWord[4] = 4

        pktWriteNWord[5] = register # register address

        i = 6
        for date in data:
            pktWriteNWord[i] = date & 255
            pktWriteNWord[i+1] = date >> 8
            i += 2

        pktWriteNWord[-1] = self.__checkSum(pktWriteNWord)

        self.__serial_port.write(bytearray(pktWriteNWord)) #write pkt to servo
        if self.prt:
            print("SEND:" + str(pktWriteNWord))



        # Sends packet to servo in order to write n data bytes into servo memory
        # register -> register address of servo
        # data     -> list of bytes to write
        # trigger  -> False -> command is directly executed, True -> command is delayed until action command
        # __pktWriteNByte = [255, 255, 0, 0, 3, 0]
        def _writeNBytePkt(self, register, data, trigger, byteNum):
            pktWriteNByte = Dynamixel.__pktWriteNByte
            pktWriteNByte[2] = self.id

            pktWriteNByte.extend([0] * (byteNum + 2))  # data byte(s) + register byte
            pktWriteNByte[3] = byteNum + 2  # length
            pktWriteNByte[5] = register  # register address

            if trigger:
                pktWriteNByte[4] = 4  # REG WRITE

            # place bytes
            # start at index 6
            for i in range(6, 6 + byteNum, 2):
                pktWriteNByte[i] = data[i - 6] & 255  # low byte
                pktWriteNByte[i + 1] = data[i - 6] >> 8  # high byte

            pktWriteNByte[-1] = self.__checkSum(pktWriteNByte)

            self.__serial_port.write(bytearray(pktWriteNByte))  # write pkt to servo
            # print("SEND:" + str(pktWriteNByte))
            Dynamixel.__pktWriteNByte = [255, 255, 0, 0, 3, 0]  # reset for some reason

        # Sends packet to servo in order to write data dword into servo memory
        # register -> register address of servo
        # data     -> list of words to write
        # trigger  -> False -> command is directly executed, True -> command is delayed until action command
        # __pktWriteWord = [255, 255, 0, 7, 3, 0, 0, 0, 0, 0, 0]
        # When Sync Writing to different registers
        def _writeNWordPkt(self, register, data, trigger, wordNum):
            pktWriteWord = self.__pktWriteWord  # copy base pkt
            pktWriteWord[2] = self.id  # place id

            if trigger:
                pktWriteWord[4] = 4  # REG WRITE

            pktWriteWord[5] = register  # place register address
            # print(data[0], data[1])
            for i in range(wordNum):
                pktWriteWord[i + 6] = data[i] & 255  # position low byte
                pktWriteWord[i + 7] = data[i] >> 8  # position high byte

            pktWriteWord[-1] = self.__checkSum(pktWriteWord)  # place check sum
            # print(pktWriteWord)
            self.__serial_port.write(pktWriteWord)  # write pkt to servo


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

