import tkinter as tk
import constants

class display2():
    def __init__(self, pointer):
        self.pointer = pointer#save resource pointer
        self.root =tk.Tk()
        self.root.state('zoomed')
        self.encoders=[]
        self.motors=[]
        self.cells=[]
        self.text=[]
        row=12
        col=10

        for encoder_no in range(10):
            newCanvas = tk.Canvas(self.root, width=120, height=20, bg="light green")
            newCanvas.configure(bg="green")
            self.encoders.append(newCanvas)
            self.encoders[encoder_no].grid(column = encoder_no,row =0)

        for motor_no in range(5):
            newCanvas = tk.Canvas(self.root, width=120, height=20, bg="MediumOrchid1")
            self.motors.append(newCanvas)
            self.motors[motor_no].grid(column = motor_no ,row =1)
            
        for cell_no in range(row*col):
            newCanvas = tk.Canvas(self.root, width=120, height=60, bg="Grey38")
            text = newCanvas.create_text(60,30, text=str(cell_no), fill="black", font=('Helvetica 8 bold'))
            self.cells.append(newCanvas)
            self.text.append(text)
            self.cells[cell_no].grid(column = (cell_no%row),row = (cell_no//row)+2)
        
        self.root.after(500,self.updator)
        self.root.mainloop()

    def updator(self):
        #update encoder states
        for i in range(constants.ENCODER_DRIVER_COUNT):
            if self.pointer.encoders[i].connection:
                self.encoders[i].configure(bg="green")
            else:
                self.encoders[i].configure(bg="light green")

        for i in range(constants.MOTOR_DRIVER_COUNT):
            if self.pointer.motors[i].connection:
                self.motors[i].configure(bg="purple")
            else:
                self.motors[i].configure(bg="MediumOrchid1")
        
        for i in range(constants.MOTOR_COUNT):
            id=self.pointer.pidControllers[i].id
            pos=self.pointer.pidControllers[i].position
            tgt=self.pointer.pidControllers[i].pid.setpoint
            pwr=self.pointer.pidControllers[i].power
            if i==0:
                print(pos)
            data=str(pos)+" "+str(id)+"\n"+str(tgt)+" "+str(pwr)
            self.cells[i].itemconfig(self.text[i], text=data)


        self.root.after(500,self.updator)
                


if __name__ == "__main__":
    display2()