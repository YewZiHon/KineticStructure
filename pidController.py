from simple_pid import PID
from serialHAL import serial_ports, SerialHal
import time
import threading
import constants

class controller():
    def __init__(self, id):
        self.id=id
        threadHandle = threading.Thread(target=self.controllerLoop, args=(),daemon=True)
        threadHandle.start()

    
    def controllerLoop(self):
        pass

def controllerStart(pointer):
    for i in range(constants.MOTOR_COUNT):
        pointer.pidControllers[i] = controller(i)