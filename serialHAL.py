import serial
import json
import sys
import glob
import time
import threading

def serial_ports():
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

class SerialHal():
    
    def __init__(self, connectionport):
        #vars
        self.readBuffer=[]
        self.sendBufffer=[]
        self.id=""
        self.connection=None
        self.mode=""
        self.add=-1
        self.position=[0,0,0,0,0,0,0,0,0,0,0,0]
        self.threadHandle=None
        self.port=""

        #start connection
        self.connection = serial.Serial(port=connectionport, baudrate=115200,parity=serial.PARITY_NONE)
        time.sleep(1)
        self.connection.reset_input_buffer()
        self.port=connectionport

        #get identity
        self.println('{"i":0}')
        identity = self.read()
        if 'i' in identity:
            identity = identity['i']
        else: 
            print("-",identity,"-")
        self.id=identity
        self.mode=identity[0]
        self.add=int(identity[1:])

        #start reading thread if encoder
        if self.mode =='E':
            self.threadHandle = threading.Thread(target=self.dataReader, args=(),daemon=True)
            self.threadHandle.start()
        print(connectionport,"done")

    def dataReader(self):
        expected=['0','1','2','3','4','5','6','7','8','9','A','B']
        while True:
            index=0
            newdata = self.read()
            for i in expected:
                try:
                    self.position[index]=newdata[i]
                except:
                    pass
                index+=1
            #print(self.id+':',self.position)

    def println(self,data):
        try:
            if self.connection.out_waiting>1:
                print("outbuff cap")
                return
    
            if "p" in data:
                pass
                #data["p"]+=255
            data = str(data)
            data=data.replace(" ","")
            data=data.replace("'","\"")
            data = data.encode('utf-8')
            self.connection.write(data)
            #self.connection.flush()
            #print(data)
        except BaseException as e:
            print("ERROR:",self.port, e)
            return
    
    def read(self):
        while True:
            data = self.connection.readline().decode("utf-8")
            if self.connection.in_waiting>1:
                print("inbuff cap")
                self.connection.reset_input_buffer()
            try:

                dict_json = json.loads(data)
                
                return dict_json
            except json.JSONDecodeError as e:
                print("JSON:", e)
