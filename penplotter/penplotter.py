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

state = enum.Enum('state', ['takePhoto', 'previewPhoto', 'gen', 'plot', 'paused'])

if not os.path.isdir(sys.path[0]+"\\temp"):
    os.makedirs(sys.path[0]+"\\temp")

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

        self.panel = tkinter.Label()
        self.btn0=tkinter.Button(self.root)
        self.btn1=tkinter.Button(self.root)
        self.btn2=tkinter.Button(self.root)

        self.panel.pack(side=tkinter.TOP, padx=10, pady=10)

        self.startStream()

        self.root.wm_title("Plotter")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def startStream(self):
        self.root.bind_all('<Escape>', None)
        self.root.bind_all('<Enter>', None)
        self.btn1.pack_forget()
        self.btn2.pack_forget()
        self.state=state.takePhoto
        self.btn0 = tkinter.Button(self.root, text="Take A Photo (Space)",command=self.takeSnapshot)
        self.btn0.pack(anchor=tkinter.S)
        self.root.bind_all('<space>', self.spaceHandle)

        self.thread = threading.Thread(target=self.videoLoop, args=(), daemon=True)
        self.thread.start()

    def videoLoop(self):
        while self.state==state.takePhoto:
            
            _, self.frame = self.vs.read()
            maxwidth, maxheight = 1600, 800
            f1 = maxwidth / self.frame.shape[1]
            f2 = maxheight / self.frame.shape[0]
            f = min(f1, f2)  # resizing factor
            dim = (int(self.frame.shape[1] * f), int(self.frame.shape[0] * f))
            self.frame = cv2.resize(self.frame, dim)

            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            
            self.panel.configure(image=image)
            self.panel.image = image

    def spaceHandle(self,_):
        self.takeSnapshot()

    def takeSnapshot(self):
        self.root.bind_all('<space>', None)
        self.filename = datetime.datetime.now().strftime("%dd%mm%Yy-%Hh%Mn%Ss")+".jpeg"
        # save the file
        print("saving",sys.path[0]+"\\temp\\"+self.filename)
        print(cv2.imwrite(sys.path[0]+"\\temp\\"+self.filename, self.frame.copy()))
        self.state=state.previewPhoto
        self.btn0.pack_forget()
        self.btn1 = tkinter.Button(self.root, text="Back(Esc)",command=self.startStream)
        self.btn1.pack(anchor=tkinter.SW, padx=10,pady=10)
        self.btn2 = tkinter.Button(self.root, text="Continue(Enter)",command=self.genGcode)
        self.btn2.pack(anchor=tkinter.SE, padx=10,pady=10)
        self.root.bind_all('<Escape>', self.startStream)
        self.root.bind_all('<Enter>', self.genGcode)
        self.root.update()
        self.root.update_idletasks()

    def genGcode(self):
        print("Gcode")

    def on_closing(self):
        self.root.destroy()
        exit()


print("Waiting for camera")
vs = cv2.VideoCapture(0)
pba = plotter(vs)
pba.root.mainloop()