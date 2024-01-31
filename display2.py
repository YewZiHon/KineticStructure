import tkinter as tk


class display2():
    def __init__(self):
        self.root =tk.Tk()
        self.root.state('zoomed')
        self.encoders=[]
        self.motors=[]
        self.cells=[]
        row=12
        col=10

        for encoder_no in range(10):
            newCanvas = tk.Canvas(self.root, width=120, height=30, bg="green")
            self.encoders.append(newCanvas)
            self.encoders[encoder_no].grid(column = encoder_no,row =0)

        for motor_no in range(5):
            newCanvas = tk.Canvas(self.root, width=120, height=30, bg="purple")
            self.motors.append(newCanvas)
            self.motors[motor_no].grid(column = motor_no ,row =1)
            
        for cell_no in range(row*col):
            newCanvas = tk.Canvas(self.root, width=120, height=60, bg="blue")
            self.cells.append(newCanvas)
            self.cells[cell_no].grid(column = (cell_no%row),row = (cell_no//row)+2)
        self.root.mainloop()


if __name__ == "__main__":
    display2()