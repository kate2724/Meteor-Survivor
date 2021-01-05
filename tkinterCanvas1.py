import tkinter as tk



class CanvasGUI:
    """Creates a canvas and draws three balls on it.  
    It then moves the balls dynamically"""

    def __init__(self):
        """Create the canvas widget and the objects to place in it"""
        
        self.rootWin = tk.Tk()
        self.rootWin.title("First Canvas example")
        
        # Create a canvas that is 500 by 500 pixels, with a yellow background
        self.canvas = tk.Canvas(self.rootWin, bg="yellow",
                             width = 500, height = 500, bd = 0)
        self.canvas.grid(row = 1, column = 1)
        # Show all of the canvas
        self.canvas.config(scrollregion= self.canvas.bbox(tk.ALL))
        
        # Make an instance variable called ballList, to hold information about
        # the balls being displayed.  Each entry in the list holds the ball's 
        # id number (assigned by the canvas widget when the ball is created) 
        # and how to move the ball

        self.ballList = []
        # Create the first, red, ball
        nextBall = self.canvas.create_oval(20, 40, 40, 60,
                                            fill = "red", outline = "black")
        self.ballList.append([nextBall, 1, 1])  # slow moving diagonally
        # Create the second, blue, ball
        nextBall = self.canvas.create_oval(70, 70, 90, 90,
                                            fill = "blue", outline = "black")
        self.ballList.append([nextBall, 2, 1]) # moves twice as far in x dim
        # Create the third, green, ball
        nextBall = self.canvas.create_oval(100, 10, 120, 30,
                                            fill = "green", outline = "black")
        self.ballList.append([nextBall, 2, 3]) # moves very fast
        
    

    def go(self):
        """Takes no inputs, and runs its own loop for the GUI.  This is so we can 
        move the balls without waiting for some user input."""
        try:
            while True:
                self.moveBalls()  # call local method to update ball positions
                self.rootWin.update_idletasks() # redraw
                self.rootWin.update() # process events
        except tk.TclError:
            pass # to avoid errors when the window is closed


    def moveBalls(self):
        """Takes no inputs, and moves the balls in the ball list.  It bounces
        back when it reaches the walls of the canvas"""
        for ballInfo in self.ballList:
            ball = ballInfo[0]
            (x0, y0, x1, y1) = self.canvas.coords(ball)
            if x1 >= 500 or x0 <= 5:
                ballInfo[1] = - ballInfo[1]
            if y1 >= 500 or y0 <= 5:
                ballInfo[2] = - ballInfo[2]
            xDist = ballInfo[1]
            yDist = ballInfo[2]
            self.canvas.move(ball, xDist, yDist)    
# end of the CanvasGUI class



# --- here it goes...

myGui = CanvasGUI()
myGui.go()
