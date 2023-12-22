from simple_pid import PID
from serialHAL import serial_ports, SerialHal
import time
import threading

def controllerStart():
    threadHandle = threading.Thread(target=controllerLoop, args=(),daemon=True)
    threadHandle.start()

def motorMap(motornum):
    col=motornum%24
    row=motornum//24
    return col,row

def revMotorMap(col,row):
    return col*24+row

def encoderMap(encnum):
    col=encnum%12
    row=encnum//12
    return col,row

def revEncoderMap(col,row):
    return col*12+row


def controllerLoop():
    ports = serial_ports()
    print(ports)  
    motorsControllers=[None,None,None,None,None,None]
    encoders=[None,None,None,None,None,None,None,None,None,None,None,None]
    for port in ports:
        ser = SerialHal(port)    
        if ser.mode == 'E':#if encoder port
            encoders[ser.add]=ser
        elif ser.mode == 'M':#if motor port
            motorsControllers[ser.add]=ser
    motorObject=[]
    for i in range(144):
        motorObject.append(PID(1, 0.1, 0.05, setpoint=0))
        motorObject[i].sample_time = 0.01
        motorObject[i].output_limits = (-255, 255)
    print(motorsControllers)
    print(encoders)
    while True:
        break

controllerLoop()