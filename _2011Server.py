
import flask
import serial
import threading
import sys
import glob
import time

class serverSerial():

    def __init__(self):
        
        try:
            self.thread = threading.Thread(target = self.loop, daemon=True)
            self.thread.start()
            
            
        except Exception as e:
            print(e)

        
        
    def serial_ports(self):
        
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

    def loop(self):
        try:
            comport = self.serial_ports()[0]
            self.serial=serial.Serial(comport, baudrate=115200)
        except:
            pass
        self.hum=100.0
        self.temp=1000.0
        self.soil=10000
        while 1:
            try:
                line = self.serial.readline()[:-2].decode()
                line=line.split(' ')
                self.hum=line[0]
                self.temp=line[1]
                self.soil=line[2]
                print(line)
            except Exception as e:
                print(e)
                self.hum=time.time()%10
            
            
            time.sleep(0.1)

app = flask.Flask(__name__)
ser = serverSerial()

@app.route("/")
def returnData():
    returnString=""
    hum = ser.hum
    temp = ser.temp
    soil = ser.soil
    returnString+=str(hum)
    returnString+=" "
    returnString+=str(temp)
    returnString+=" "
    returnString+=str(soil)
    print(returnString)

    return returnString



app.run(debug=1,port=80)