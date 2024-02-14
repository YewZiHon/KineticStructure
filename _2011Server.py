try:
    import flask
    import serial
except Exception as e:
    print(e)
    import pip
    pip.main(['install', "flask", "pyserial"])
import threading
import sys
import glob

class serverSerial():
    def __init__(self):
        
        try:
            comport = self.serial_ports()[0]
            self.serial=serial.Serial(comport, baudrate=115200)
            self.thread = threading.Thread(target = self.loop, daemon=True)
            self.thread.start()
        except Exception as e:
            print(e)
        
        self.hum=100
        self.temp=1000
        self.soil=10000
        

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
        while 1:
            line = self.serial.readline()
            print(line)
            line=line.split(b' ')
            if len(line)==3:
                self.hum=float(line[0])
                self.temp=float(line[1])
                self.soil=int(line[2])
            else:
                continue

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

    return returnString


app.run(debug=1,port=80)