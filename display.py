import turtle    
import threading

class display():
    def __init__(self, motorHandel):
        self.motorHandel = motorHandel
        self.loop = threading.Thread(target=self.display_loop, daemon=True)
        self.loop.start()
        print("run")

    def display_loop(self):
        print("loop")
        turtle.delay(0)
        turtle.tracer(0, 0)
        

        #set to maximise
        turtle.setup(width = 1.0, height = 0.95,  startx=0, starty=0)
        offsetx = -turtle.window_width()/2
        offsety = -turtle.window_height()/2
    
        turtle.speed(0)
        
        TOP_OFFSET = 30
        CELL_HEIGHT = (turtle.window_height()-60)/10
        LEFT_OFFSET = 30
        CELL_WIDTH = (turtle.window_width()-60)/12

        #draw turtle grid
        turtle.speed(0)
        turtle.pu()
        for i in range(10+1):
            turtle.goto(offsetx+LEFT_OFFSET,offsety+TOP_OFFSET+CELL_HEIGHT*i)
            turtle.pd()
            turtle.goto(offsetx+LEFT_OFFSET+12*CELL_WIDTH,offsety+TOP_OFFSET+CELL_HEIGHT*i)
            turtle.pu()

        for i in range(12+1):
            turtle.goto(offsetx+LEFT_OFFSET+i*CELL_WIDTH,offsety+TOP_OFFSET)
            turtle.pd()
            turtle.goto(offsetx+LEFT_OFFSET+i*CELL_WIDTH,offsety+TOP_OFFSET+CELL_HEIGHT*10)
            turtle.pu()
        turtle.update()
        #end draw turtle grid

        def getxy(index):
            row = index%12
            col = 10-index//12
            x = TOP_OFFSET+row*CELL_WIDTH+offsetx
            y = LEFT_OFFSET+col*CELL_HEIGHT+offsety
            return x,y

        
        #plot names 
        NAME_X_OFFSET=5
        NAME_Y_OFFSET=-23

        turtle.color('blue')

        for cell_index in range(120):
            name = chr(ord("A")+cell_index//12)+str(cell_index%12+1)
            #print(cell_index,name)
            xcord, ycord = getxy(cell_index)
            xcord+=NAME_X_OFFSET
            ycord+=NAME_Y_OFFSET
            turtle.goto(xcord,ycord)
            turtle.write(name, font = ("Arial", 14, "normal"))
        turtle.ht()
        turtle.update()

        #plot names end


        ENCODER_X_OFFSET=5
        ENCODER_Y_OFFSET=-100

        data = turtle.Turtle()
        data.ht()
        data.pu
        data.speed(0)
        data._tracer(0, 0)
        
        while True:
            print("run2")
            cell_counter=0
            data.clear()
            for i in self.motorHandel:
                if i is not None:
                    #read the actual values
                    pass
                else:
                    encoder="encval"
                    target="tgtval"
                    pwm="pwmval"
                    

                #plot the values
                xcord, ycord = getxy(cell_counter)
                xcord+=ENCODER_X_OFFSET
                ycord+=ENCODER_Y_OFFSET
                data.goto(xcord, ycord)
                data.write(str(encoder))
                data.goto(xcord, ycord+20)
                data.write(str(target))
                data.goto(xcord, ycord+40)
                data.write(str(cell_counter))

                data._update()
                
                cell_counter+=1




if __name__ =="__main__":
    display([None for i in range(12)])
    while True:
        pass