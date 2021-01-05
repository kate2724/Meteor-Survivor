import tkinter as tk


# ------------------ GUI class and methods ----------------
class Bullet:
    def __init__(self, canvas, x0, y0, x1, y1, movement):
        xavg = (x0 + x1) / 2
        self.bullet = canvas.create_line(xavg, y0, xavg, y1, fill='white', arrow=tk.FIRST)
        self.movement = movement

    def move(self, canvas):
        canvas.move(self.bullet, self.movement[0], self.movement[1])


class BasicGui:
    """Creates a canvas, and draws a square on it that the user can control"""

    def __init__(self):
        """Creates Canvas widget, and places a rectangle on it."""
        self.mainWin = tk.Tk()
        self.mainWin.title("Block Survivor")

        # creates canvas that is 1000 x 1000 pixels, with a black background
        self.myCanvas = tk.Canvas(self.mainWin)
        self.myCanvas["width"] = 1000
        self.myCanvas["height"] = 1000
        self.myCanvas["bg"] = "black"
        self.myCanvas.grid(row=10, column=0)

        self.bullets = []  # store bullets
        self.tick_loop()  # start the tick loop

        # creates a rectangle on the canvas with its top left corner at position (475,750) and its bottom right corner
        # at position (525,800)
        self.r1 = self.myCanvas.create_rectangle(475, 750, 525, 800, fill="white")

        # binds the a, d, and space keys to the function, and call the function moveCallback
        self.mainWin.bind("<a>", self.go_left)
        self.mainWin.bind("<d>", self.go_right)
        self.mainWin.bind("<space>", self.space_key)

    def run(self):
        """This function runs the class, causing the program to go into effect"""
        self.mainWin.mainloop()

    def go_left(self, event):
        self.myCanvas.move(self.r1, -20, 0)

    def go_right(self, event):
        self.myCanvas.move(self.r1, 20, 0)

    def space_key(self, event=0):
        x0, y0, x1, y1 = self.myCanvas.coords(self.r1)
        self.bullets.append(Bullet(self.myCanvas, x0, y0, x1, y1, (0, -10)))

    def tick_loop(self):
        remove_list = []
        for enum, bullet in enumerate(self.bullets):
            coords = self.myCanvas.coords(bullet.bullet)
            if coords[1] < 0 or coords[0] < 0:
                remove_list.append(enum)
                self.myCanvas.delete(bullet.bullet)
            else:
                bullet.move(self.myCanvas)

        for enum, index in enumerate(remove_list):
            self.bullets.pop(index - enum)

        self.mainWin.after(int(1000 / 30), self.tick_loop)


# ------------------ Main program ----------------------

myGui = BasicGui()
myGui.run()

