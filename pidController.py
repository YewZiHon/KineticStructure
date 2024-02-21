from simple_pid import PID
from serialHAL import serial_ports, SerialHal
import time
import threading
import constants

class controller():
    def __init__(self, id, pointer):
        self.id=id
        self.pointer=pointer
        self.position=0
        self.target=0
        self.power=0
        self.encoderDriver=id//12
        self.encoderPort=id%12
        self.motorDriver=id//24
        self.motorPort=id&24
        self.enc_OK=False

        self.pid=PID(1, 0.1, 0.05, setpoint=300, sample_time=0.1)
        self.pid.output_limits=(-127,127)


        threadHandle = threading.Thread(target=self.controllerLoop, args=(),daemon=True)
        threadHandle.start()


    
    def controllerLoop(self):
        while True:
            #get position value
            if self.pointer.encoders[self.encoderDriver]:
                self.position=self.pointer.encoders[self.encoderDriver].position[self.encoderPort]
                self.enc_OK=True
            else:
                self.enc_OK=False

            #calc power
            self.power=round(self.pid(self.position))


            #get motor
            if self.pointer.motors[self.motorDriver]:
                self.position=self.pointer.motors[self.motorDriver].writeData(self.id, self.power)


def controllerStart(pointer):
    for i in range(constants.MOTOR_COUNT):
        pointer.pidControllers[i] = controller(i,pointer)