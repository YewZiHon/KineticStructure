from simple_pid import PID
from serialHAL import serial_ports, SerialHal
import time
import threading

def controllerStart():
    threadHandle = threading.Thread(target=controllerLoop, args=(),daemon=True)
    threadHandle.start()

def motorMap(motornum):
    col=motornum%6#controller
    row=motornum//6#motor
    return col,row

def revMotorMap(col,row):
    return col*6+row

def encoderMap(encnum):
    col=encnum%12
    row=encnum//12
    return col,row

def revEncoderMap(col,row):
    return col*12+row

def getEncoders(encoders):
    array=[]
    for encoderDriver in encoders:
        if encoderDriver:
            array+=encoderDriver.position
        else:
            array+=[0,0,0,0,0,0,0,0,0,0,0,0]
    return array

def controllerLoop():
    #setup
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
    #homing
    for i in range(144):#start all motors
        con, mot = motorMap(i)
        data = {'m':mot,'p':127}
        if motorsControllers[con]:
            motorsControllers[con].println(data)
    time.sleep(1)

    #init accumulators
    startTime=time.time()
    lastTime=[startTime for i in range(144)]
    lastPosition=[0 for i in range(144)]
    reached=[0 for i in range(144)]
    
    while True:
        if time.time()-startTime>20:
            print('timeout')
            break
        if 0 not in reached:
            break

        newpositions = getEncoders(encoders)
        #print(newpositions)
        currtime=time.time()
        for i in range(144):
            if newpositions[i]!=lastPosition[i]:
                lastTime[i]=currtime
                newpositions[i]=lastPosition[i]
            if currtime - lastTime[i]>100:
                con,mot = motorMap(i)
                reached[i]=1
                data = {'m':mot,'p':0}
                if motorsControllers[con]:
                    print(i,"reached")
                    motorsControllers[con].println(data)



    #control loop
    while True:
        break

controllerLoop()