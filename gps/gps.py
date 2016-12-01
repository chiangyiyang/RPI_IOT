import serial


def getdata(port):
    # open the serial port
    port.open()
    # check that the port is open
    if port.isOpen():
        # read 16 lines
        line = []
        for i in range(1, 16):
            line.append(port.readline())
        # close the serial port
    port.close()
    # discard the first line (sometimes it contains rubbish, so just always discard it)
    del line[0]
    # return the list of lines
    return line


def outputdata(data):
    # print the list of lines
    for i in range(0, len(data)):
        print data[i]


def initialise():
    # initialise serial port settings
    Port = serial.Serial()
    Port.baudrate = 9600
    Port.port = "/dev/ttyAMA0"
    Port.xonxoff = 1
    # return the port as an object we can use
    return Port


# main program starts here
sPort = initialise()
data = getdata(sPort)
outputdata(data)
# end
