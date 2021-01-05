import tkinter as tk
import random

# ------------------ GUI class and methods ----------------

class Bullet:
    def __init__(self, canvas, x0, y0, x1, y1, movement):
        xavg = (x0 + x1)/ 2
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
        self.myCanvas.grid(row=0, column=0)

        self.n = 0
        self.level = 1  # initializes game level

        self.bullets = []  # store bullets
        self.enemyList = []  # store enemies

        self.tick_loop()  # start the tick loop

        # self.make_enemies()
        x0 = random.randrange(0, 1000)
        x1 = x0 + 50
        self.enemy = self.myCanvas.create_rectangle(x0, 0, x1, 50, fill="white")
        self.enemyList.append(self.enemy)
        self.enemies_fall()

        # creates a rectangle on the canvas with its top left corner at position (475,750) and its bottom right corner
        # at position (525,800)
        self.r1 = self.myCanvas.create_rectangle(475, 750, 525, 800, fill="white")

        # binds the a, d, and space keys to the function, and calls their respective callback functions
        self.mainWin.bind("<a>", self.go_left)
        self.mainWin.bind("<d>", self.go_right)
        self.mainWin.bind("<space>", self.space_key)

    def run(self):
        """This function runs the class, causing the program to run."""
        self.mainWin.mainloop()

    # def make_enemies(self):
    #     for i in range(self.level * 3): # creates certain amount of enemies based on level, and draws them on canvas
    #         print(i)
    #         x0 = random.randrange(0, 1000)
    #         x1 = x0 + 50
    #         self.enemy = self.myCanvas.create_rectangle(x0, 0, x1, 50, fill="white")
    #         self.enemyList.append(self.enemy)
    #     self.enemies_fall()

        # x0 = random.randrange(0, 1000)
        # x1 = x0 + 50
        # self.enemy = self.myCanvas.create_rectangle(x0, 0, x1, 50, fill="white")
        # self.enemyList.append(self.enemy)
        # self.enemies_fall()

    def enemies_fall(self):
        """Moves all the enemy shapes in the enemy List. If they go
        out of bounds they are taken off the canvas and taken off the list
        If not, they are moved down the canvas."""
        # x0 = random.randrange(0, 1000)
        # x1 = x0 + 50
        # self.enemy = self.myCanvas.create_rectangle(x0, 0, x1, 50, fill="white")
        # self.enemyList.append(self.enemy)
        enemyCoords = self.myCanvas.coords(self.enemy)
        if enemyCoords[3] > 250:
            self.n = self.n + 1
            x0 = random.randrange(0, 1000)
            x1 = x0 + 50
            self.enemy = self.myCanvas.create_rectangle(x0, 0, x1, 50, fill="white")
            self.enemyList.append(self.enemy)
            if self.n > 1:
                self.level = self.level + 1
                self.n = 0
                print(f"Level {self.level}!")
        if self.level == 11:
            self.mainWin.quit()


        for enum, enemy in enumerate(self.enemyList):
            coords = self.myCanvas.coords(enemy)
            if len(coords) > 1:
                if coords[3] >= 1000:
                    self.enemyList.pop(enum)
                    self.myCanvas.delete(enemy)
                else:
                    self.myCanvas.move(enemy, 0, 1)

            for bulletEnum, bullet in enumerate(self.bullets): # deletes enemy if bullet in same position
                bulletCoords = self.myCanvas.coords(bullet.bullet)
                if coords[3] >= bulletCoords[3]:
                    if coords[0] <= bulletCoords[0] and coords[2] >= bulletCoords[2]:
                        self.enemyList.pop(enum)
                        self.myCanvas.delete(enemy)
                        self.myCanvas.delete(bullet.bullet)
                        self.bullets.pop(bulletEnum)

            # if not self.enemyList: # for levels 2 to 10, reacreates enemies and drops them. When all enemies of a level
            #     # off canvas, repeat for next level.
            #     self.level = self.level + 1
            #     if self.level == 11:
            #         break
            #     for i in range(self.level * 3):
            #         x0 = random.randrange(0, 1000)
            #         x1 = x0 + 50
            #         self.enemy = self.myCanvas.create_rectangle(x0, 0, x1, 50, fill="white")
            #         self.enemyList.append(self.enemy)
            #     self.enemies_fall()
        self.mainWin.after(5, self.enemies_fall)

    def go_left(self, event):
        x0, y0, x1, y1 = self.myCanvas.coords(self.r1)
        if x0 > 0:
            self.myCanvas.move(self.r1, -20, 0)

    def go_right(self, event):
        x0, y0, x1, y1 = self.myCanvas.coords(self.r1)
        if x1 < 1000:
            self.myCanvas.move(self.r1, 20, 0)

    def space_key(self, event=0):
        x0, y0, x1, y1 = self.myCanvas.coords(self.r1)
        self.bullets.append(Bullet(self.myCanvas, x0, y0, x1, y1, (0, -10)))

    def tick_loop(self):
        remove_list = []
        for enum, bullet in enumerate(self.bullets):
            coords = self.myCanvas.coords(bullet.bullet)
            if coords[1] < 0:
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
