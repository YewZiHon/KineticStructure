import serial
import sys
import glob
import time
import threading

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def init():
    #get ports
    ports = serial_ports()
    serHandel=[None,None]#tc1, board
    #find ports
    for port in ports:
        #attempt to open port
        print("opening",port)
        ser=serial.Serial(port,250000,timeout=1)
        time.sleep(2)
        ser.write(b"\n")
        ser.flush()
        ser.reset_input_buffer()
        print("opened",port)
        ser.write(b"M118 TC1\n\n")
        tries=0
        while tries<10:
            data = ser.readline()
            print("raw", data)
            data=data.decode("utf-8")
            if "TC1" in data:
                print("TC1", port)
                if serHandel[0]:
                    raise Exception("multiple printers???")
                serHandel[0]=ser
                break
            elif len(data)==65:#64+\n
                print("board",port)
                if serHandel[1]:
                    raise Exception("multiple boards???")
                serHandel[1]=ser
                break
            else:
                print("data",data,port)
                tries+=1
    return serHandel

class printerHandle():
    def __init__(self, portHandle):
        self.ser = portHandle
        self.ser.write(b"G28\n")
    
    def goto(self,x=None, y=None, z=None):

        #move to nowhere
        if x==None and y==None and z==None:
            return
        
        data = "G0 F100000 "

        if x!=None:
            data+="X"
            data+=str(x)
        
        if y!=None:
            data+="Y"
            data+=str(y)

        if z!=None:
            data+="Z"
            data+=str(z)

        self.ser.write(data)
        
class boardHandle():
    def __init__(self, portHandle):
        self.ser = portHandle
        self.states="0"*64
        self.thread = threading.Thread(target = self.boardLoop, daemon=True)
        self.thread.start()

    def boardLoop(self):
        while True:
            data = self.ser.readline()
            if data != "":
                self.states = data[0:64]



if __name__ =="__main__":
    tc1,board = init()
    if not tc1 or not board:
        raise Exception("Not connected: (tc1, board)",tc1,board)
    tc1 = printerHandle(tc1)
    board = boardHandle(board)

