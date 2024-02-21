import serial
import json
import sys
import glob
import time
import threading
import constants

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
    """
    __init__()
    @param, connection port
    attempt to connect

    datareader()
    loop only rinning if encoder

    println()
    print to serial device

    read()
    read one line of data
    """
    
    def __init__(self, id):
        #vars
        self.readBuffer=[]
        self.sendBufffer=[]
        self.id=id
        self.connection=None
        self.mode=id[0]
        self.add=int(id[1])
        self.position=[0,0,0,0,0,0,0,0,0,0,0,0]
        self.threadHandle=None
        self.port=""

    def attach(self, connectionport):
        if self.connection:
            print("Conflicting connection!!!",connectionport)
            return
        print("attach", self.id)
        try:
            #start connection
            self.connection = serial.Serial(port=connectionport, baudrate=115200,parity=serial.PARITY_NONE)
            time.sleep(1)
            self.connection.reset_input_buffer()
            self.port=connectionport

            #start reading thread if encoder
            if self.mode =='E':
                self.threadHandle = threading.Thread(target=self.dataReader, args=(),daemon=True)
                self.threadHandle.start()
            print(connectionport,"done")
        except Exception as e:
            print(e)
            try:
                self.connection.close()
            except:
                pass
            self.connection=None

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

    def writeData(self,id,pwr):
        self.println(json.dumps({"M":id,"P":pwr}))

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
    
    def read(self):
        while True:
            try:
                data = self.connection.readline().decode("utf-8")
                if self.connection.in_waiting>1:
                    print("inbuff cap")
                    self.connection.reset_input_buffer()
                try:

                    dict_json = json.loads(data)
                    
                    return dict_json
                except json.JSONDecodeError as e:
                    print("JSON:", e)
            except:
                try:
                    self.connection.close()
                except:
                    pass
                self.connection=None


class serialConnector():
    def __init__(self, pointer):
        self.pointer=pointer

        #start encoder handles
        for i in range(constants.ENCODER_DRIVER_COUNT):
            self.pointer.encoders[i]=SerialHal("E"+str(i))
        #start motor handles
        for i in range(constants.MOTOR_DRIVER_COUNT):
            self.pointer.motors[i]=SerialHal("M"+str(i))

        threadHandle = threading.Thread(target=self.connectorLoop, args=(),daemon=True)
        threadHandle.start()

    def connectorLoop(self):
        
        while True:
            try:
                ports = serial_ports()
                if not ports:
                    continue
                for port in ports:
                    try:
                        connection = serial.Serial(port=port, baudrate=115200,parity=serial.PARITY_NONE, timeout=1)
                        time.sleep(1)
                        connection.reset_input_buffer()

                        #get identity
                        connection.write(bytearray('{"i":0}',"utf-8"))
                        identity = connection.readline().decode("utf-8")
                        identity=json.loads(identity)
                        identity=identity['i']
                        #print(identity)
                        
                        mode=identity[0]
                        add=int(identity[1])
                        connection.close()
                        if mode=="E":
                            self.pointer.encoders[add].attach(port)
                            #print("attach ", identity)
                        elif mode=="M":
                            self.pointer.motors[add].attach(port)
                            #print("attach ", identity)
                    except Exception as e:
                        print(e)

            except Exception as e:
                print(e)
                    
