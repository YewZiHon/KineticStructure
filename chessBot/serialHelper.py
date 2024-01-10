import serial
import sys
import glob
import time

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
                break
            elif len(data)==65:#64+\n
                print("board",port)
                break
            else:
                print("data",data,port)
                tries+=1




if __name__ =="__main__":
    init()