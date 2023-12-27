import cv2 as cv
from tkinter import *
from tkinter import ttk
import threading


while True:
    #setup tkinter
    root = Tk()
    width= root.winfo_screenwidth()               
    height= root.winfo_screenheight()               
    root.geometry("%dx%d" % (width, height))
    root.title("Plotter")
    frm = ttk.Frame(root, padding=10)
    frm.pack(side=CENTER)
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()
    print("done")
    #get an image

        #check if image is fine

    #convert to g code
    #start plotting 
