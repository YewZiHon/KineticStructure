# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter
import threading
import datetime
import cv2
import os
import sys
import enum
import time
import serial
import glob
from rembg import remove


state = enum.Enum('state', ['takePhoto', 'previewPhoto', 'gen', 'plot', 'paused'])

if not os.path.isdir(sys.path[0]+"\\temp"):
    os.makedirs(sys.path[0]+"\\temp")
if not os.path.isdir(sys.path[0]+"\\temp\\img"):
    os.makedirs(sys.path[0]+"\\temp\\img")
if not os.path.isdir(sys.path[0]+"\\temp\\dot"):
    os.makedirs(sys.path[0]+"\\temp\\dot")
if not os.path.isdir(sys.path[0]+"\\temp\\gcode"):
    os.makedirs(sys.path[0]+"\\temp\\gcode")

class plotter:
    def __init__(self, vs):
# store the video stream object and output path, then initialize
# the most recently read frame, thread for reading frames, and
# the thread stop event
        self.vs = vs
        self.frame = None
        self.thread = None
        self.state=state.takePhoto
        # initialize the root window and image panel
        self.root = tkinter.Tk()              
        self.root.state('zoomed')
        self.root.configure(bg='light sky blue')
        self.imgSize=800,800

        self.panel = tkinter.Label()
        self.btn0=tkinter.Button(self.root)
        self.btn1=tkinter.Button(self.root)
        self.btn2=tkinter.Button(self.root)

        self.panel.pack(side=tkinter.TOP, padx=10, pady=10)

        self.startStream()

        self.root.wm_title("Plotter")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def startStream(self,_=None):
        self.root.bind('<Escape>', None)
        self.btn1.pack_forget()
        self.btn2.pack_forget()
        self.state=state.takePhoto
        self.btn0 = tkinter.Button(self.root, text="Take A Photo (Space)",command=self.takeSnapshot)
        self.btn0.pack(anchor=tkinter.S)
        self.root.bind('<space>', self.spaceHandle)

        self.thread = threading.Thread(target=self.videoLoop, args=(), daemon=True)
        self.thread.start()

    def videoLoop(self):
        while self.state==state.takePhoto:
            
            _, self.frame = self.vs.read()
            maxwidth, maxheight = self.root.winfo_width()-100, self.root.winfo_height()-150
            f1 = maxwidth / self.frame.shape[1]
            f2 = maxheight / self.frame.shape[0]
            f = min(f1, f2)  # resizing factor
            dim = (int(self.frame.shape[1] * f), int(self.frame.shape[0] * f))
            self.frame = cv2.resize(self.frame, dim)
            self.imgSize=int(self.frame.shape[1] * f), int(self.frame.shape[0] * f)

            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image=cv2.flip(image, 1)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            
            self.panel.configure(image=image)
            self.panel.image = image

    def spaceHandle(self,_):

        self.takeSnapshot()

    def takeSnapshot(self):
        self.root.bind('<space>', None)
        self.filename = datetime.datetime.now().strftime("%dd%mm%Yy-%Hh%Mn%Ss")
        # save the file
        print("saving",sys.path[0]+"\\temp\\img\\"+self.filename+".jpeg")
        
        print(cv2.imwrite(sys.path[0]+"\\temp\\img\\"+self.filename+".jpeg", self.frame))
        self.state=state.previewPhoto
        self.btn0.pack_forget()
        self.btn1 = tkinter.Button(self.root, text="Back(Esc)",command=self.startStream)
        self.btn1.pack(anchor=tkinter.SW, padx=10,pady=10)
        print("bind1")
        self.btn2 = tkinter.Button(self.root, text="Continue(Space)",command=self.genGcode)
        self.btn2.pack(anchor=tkinter.SE, padx=10,pady=10)
        self.root.bind('<Escape>', self.startStream)
        print("bind2")
        self.root.bind('<space>', self.genGcode)
        self.root.update()
        self.root.update_idletasks()
    
    def preprocess(self):
        image=cv2.imread(sys.path[0]+"\\temp\\img\\"+self.filename+".jpeg")
        
        maxwidth, maxheight = 1600,800
        f1 = maxwidth / image.shape[1]
        f2 = maxheight / image.shape[0]
        f = min(f1, f2)  # resizing factor
        dim = (int(image.shape[1] * f), int(image.shape[0] * f))
        image = cv2.resize(image, dim)

        center = image.shape
        w=min(center[0],center[1])
        x = center[1]/2 - w/2
        y = center[0]/2 - w/2


        image = image[int(y):int(y+w), int(x):int(x+w)]

        image=remove(image)

        image=cv2.Canny(image,1,50)
    
        cv2.imwrite(sys.path[0]+"\\temp\\img\\"+self.filename+"canny.bmp",image)

        return

    def genGcode(self,_=None):
        if self.state ==state.gen:
            return
        self.state=state.gen
        self.root.bind('<Escape>', None)
        self.root.bind('<space>', None)
        self.btn1.pack_forget()
        self.btn2.pack_forget()
        self.btn1.update_idletasks()
        self.btn2.update_idletasks()

        print("Gcode")

        self.preprocess()


        img=cv2.imread(sys.path[0]+"\\generating.jpg")
        img=cv2.resize(img,self.imgSize)
        generating = Image.fromarray(img)
        generating = ImageTk.PhotoImage(generating)
        
        self.panel.configure(image=generating)
        self.panel.image = generating
        self.panel.update_idletasks()

        start=time.time()
        os.startfile(
            "\""+sys.path[0]+"\\potrace.exe\"",arguments="\""+sys.path[0]+"\\temp\\img\\"+self.filename+"canny.bmp\" "+
            "-o\""+sys.path[0]+"\\temp\\img\\"+self.filename+".svg\" --backend svg --width 800pt --height 800pt --opttolerance 0.4 "
        )
        while not os.path.exists(sys.path[0]+"\\temp\\img\\"+self.filename+".svg"):
            pass
        time.sleep(0.5)

        os.startfile(
            "\""+sys.path[0]+"\\svg2gcode.exe\"",arguments=
            "--circular-interpolation true --feedrate 100000 --tolerance 1 --on \"G0 Z0\" --off \"G0 Z2\" --out "+
            "\""+sys.path[0]+"\\temp\\gcode\\"+self.filename+".gcode\" "+
            "\""+sys.path[0]+"\\temp\\img\\"+self.filename+".svg\""
        )
        while not os.path.exists(sys.path[0]+"\\temp\\gcode\\"+self.filename+".gcode"):
            pass
        time.sleep(0.5)

        i=open(sys.path[0]+"\\start.gcode",'r')
        initgc=i.read()
        i.close()
        with open(sys.path[0]+"\\temp\\gcode\\"+self.filename+".gcode", 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(initgc + '\n' + content)
        

        preview = Image.fromarray(cv2.bitwise_not(cv2.imread(sys.path[0]+"\\temp\\img\\"+self.filename+"canny.bmp")))
        preview = ImageTk.PhotoImage(preview)
        
        self.panel.configure(image=preview)
        self.panel.image = preview
        self.panel.update_idletasks()

        print("gcode",time.time()-start)
        print("Gen done")
        self.state=state.plot
        self.thread = threading.Thread(target=self.sendGcode, args=(), daemon=True)
        self.thread.start()
        self.btn1 = tkinter.Button(self.root, text="Pause",command=self.pause)
        self.btn1.pack(anchor=tkinter.SW, padx=10,pady=10)
        self.btn2 = tkinter.Button(self.root, text="Stop",command=self.stop)
        self.btn2.pack(anchor=tkinter.SE, padx=10,pady=10)
        #self.thread.start()
        #self.sendGcode()
        
    def pause(self):
        if self.state==state.plot:
            self.state=state.paused
        elif self.state==state.paused:
            self.state=state.plot
        
    def stop(self):
        if self.state==state.plot or self.state==state.paused:
            self.state=state.takePhoto

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

    def sendGcode(self):
        #open serial
        ports = self.serial_ports()

        if ports == []:
            print("Error opening serial")
            time.sleep(5)
            self.state=state.takePhoto
            self.startStream()
            return
        print("ports",ports)
        s = serial.Serial(ports[0],115200)

        f = open(sys.path[0]+"\\temp\\gcode\\"+self.filename+".gcode",'r')

        s.write(b"\r\n\r\n") # Hit enter a few times to wake the Printrbot
        time.sleep(2)   # Wait for Printrbot to initialize
        s.flushInput()  # Flush startup text in serial input

        while True:
            if self.state==state.plot:
                #send g code
                l=f.readline()
                l=l.replace("G1","G0")
                l = l.strip() # Strip all EOL characters for streaming
                if  (l.isspace()==False and len(l)>0) :
                    print ('Sending:',  l)
                    s.write(bytearray(l + '\n','utf-8')) # Send g-code block
                    grbl_out = s.readline() # Wait for response with carriage return
                    print (grbl_out.strip())
                
            elif self.state==state.paused:
                time.sleep(0.1)
                pass
            elif self.state==state.takePhoto or self.state==state.previewPhoto or self.state==state.gen:
                break

        self.state=state.takePhoto
        self.startStream()
        return

    def on_closing(self):
        self.root.destroy()
        exit()


print("Waiting for camera")
vs = cv2.VideoCapture(0)
pba = plotter(vs)
pba.root.mainloop()