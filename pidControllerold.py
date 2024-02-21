from simple_pid import PID
from serialHAL import serial_ports, SerialHal
import time
import threading

def controllerStart():
    threadHandle = threading.Thread(target=controllerLoop, args=(),daemon=True)
    threadHandle.start()

def motorMap(motornum):
    row=motornum%24#controller
    col=motornum//24#motor
    return col,row

def revMotorMap(col,row):
    return col*24+row

def encoderMap(encnum):
    row=encnum%12
    col=encnum//12
    return col,row

def revEncoderMap(col,row):
    return col*12+row

def getEncoders(encoders):
    array=[]
    addr=[]
    for encoderDriver in encoders:
        if encoderDriver:
            array.extend(encoderDriver.position)
        else:
            array.extend([1,1,1,1,1,1,1,1,1,1,1,1])
        
    
    return array
  
def controllerLoop():
    pass

controllerLoop()