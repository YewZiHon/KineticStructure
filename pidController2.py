from simple_pid import PID
#from serialHAL import serial_ports, SerialHal
import time
import threading
import constants

class controller():
    def __init__(self, id, pointer):
        self.id=id
        self.pointer=pointer
        self.position=0
        self.power=0
        self.encoderDriver=id//12
        self.encoderPort=id%12
        self.motorDriver=id//24
        self.motorPort=id&24
        self.enc_OK=False

        self.pid=PID(1, 0.1, 0.05, setpoint=300, sample_time=0.1)
        self.pid.output_limits=(-127,127)


class controllers():

    def __init__(self, pointer):
        self.pointer=pointer
        for i in range(constants.MOTOR_COUNT):
            self.pointer.pidControllers[i] = controller(i,pointer)
        threadHandle = threading.Thread(target=self.controllerLoop, args=(),daemon=True)
        threadHandle.start()

    def controllerLoop(self):
            while True:
                for i in range(constants.MOTOR_COUNT):
                    controller=self.pointer.pidControllers[i]
                    try:
                        #get position value
                        if i==0:
                            controller.position=self.pointer.encoders[controller.encoderDriver].position[controller.encoderPort]
                            #print(controller.position)
                            enc_OK=True
                        else:
                            enc_OK=False

                        #calc power
                        if enc_OK:
                            controller.power=round(controller.pid(controller.position))

                        else:
                            controller.power=0

                        #get motor
                        
                        if self.pointer.motors[controller.motorDriver].connection:
                            controller.position=self.pointer.motors[controller.motorDriver].writeData(controller.id, controller.power)
                        else:
                            time.sleep(1)
                            
                    except BaseException as e:
                        print(e)