
import tkinter as tk
import random

class CanvasGUI3:

    def __init__(self):
        self.rootWin = tk.Tk()
        self.rootWin.title("Third Canvas example: timing")
        
        
        # Create a canvas object that is 500 by 500 pixels wide, with a yellow background
        self.canvas = tk.Canvas(self.rootWin, bg="yellow",width = 500, height = 500, bd = 0)
        self.canvas.grid(row = 1, column = 1)
        # Show all of the canvas
        self.canvas.config(scrollregion= self.canvas.bbox(tk.ALL))

        
        # Create an instance variable to hold the ball's id
        self.ball = self.canvas.create_oval(250, 250, 260, 260, fill = 'blue')


        
    def go(self):
        """Takes no inputs, starts the ball moving, and runs the main loop"""
        self.moveBall()
        self.rootWin.mainloop()


    def moveBall(self):
        """Takes no inputs, and moves the ball in the ball list.  It bounces
        back when it reaches the walls of the canvas"""
        self.canvas.move(self.ball, 10, 0)    
        self.rootWin.after(50, self.moveBall)
                
# end of class CanvasGUI


# --- here it goes...

myGui = CanvasGUI3()
myGui.go()
