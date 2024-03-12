import serialHAL
import display2
import constants
import pidController2
import time

class Pointer():
    def __init__(self):
        self.motors=[None,None,None,None,None]
        self.encoders=[None,None,None,None,None,None,None,None,None,None]
        self.pidControllers=[None for i in range(constants.MOTOR_COUNT)]

pointer=Pointer()

serialHAL.serialConnector(pointer)
pidController2.controllers(pointer)
display2.display2(pointer)
while True:
    time.sleep(1000)
