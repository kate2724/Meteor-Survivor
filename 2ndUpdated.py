import tkinter as tk
import random
import winsound



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
        self.myCanvas["width"] = 750
        self.myCanvas["height"] = 750
        self.myCanvas["bg"] = "black"
        self.myCanvas.grid(row=0, column=0)

        self.enemyCount = 0
        self.bulletCount = 0
        self.hitCount = 0

        self.level = 1  # initializes game level
        self.initialEnemyAmount = 10
        self.enemiesRemaining = self.initialEnemyAmount
        self.timeApartEnemies = 2000
        self.winning = True

        self.bullets = []  # store bullets
        self.enemyList = []  # store enemies

        self.tick_loop()  # start the tick loop

        # Start Button
        self.startButton = tk.Button(self.mainWin, text='Click to Start', padx=40, pady=20, bg='white',
                                     command=lambda: [self.create_enemy(), self.enemies_fall(), self.playMusic()])
        self.startButton.configure(width=10, activebackground="#33B5E5")
        self.startButton_window = self.myCanvas.create_window(395, 350, window=self.startButton)

        self.endButton = tk.Button(self.mainWin, text='Quit', padx=40, pady=20, bg='white',
                                   command=self.mainWin.destroy)
        self.endButton.configure(width=10, activebackground="#33B5E5")
        self.endButton_window = self.myCanvas.create_window(395, 450, window=self.endButton)

        # creates a rectangle on the canvas with its top left corner at position (475,750) and its bottom right corner
        # at position (525,800)
        self.r1 = self.myCanvas.create_rectangle(375, 700, 425, 750, fill="white")

        # binds the a, d, and space keys to the function, and calls their respective callback functions
        self.mainWin.bind("<Left>", self.go_left)
        self.mainWin.bind("<Right>", self.go_right)
        self.mainWin.bind("<a>", self.go_left)
        self.mainWin.bind("<d>", self.go_right)
        self.mainWin.bind("<space>", self.space_key)

    def restart(self):
        # self.loseLabel.destroy()
        # self.restartButton.destroy()
        # self.endButton.destroy()

        self.enemyCount = 0
        self.bulletCount = 0
        self.hitCount = 0

    #     self.level = 1  # initializes game level
    #     self.initialEnemyAmount = 10
    #     self.enemiesRemaining = self.initialEnemyAmount
    #     self.timeApartEnemies = 2000
    #     self.winning = True
    #
    #     self.bullets = []  # store bullets
    #     self.enemyList = []  # store enemies
    #
    #     self.tick_loop()  # start the tick loop
    #
    #     # Start Button
    #     self.startButton = tk.Button(self.mainWin, text='Click to Start', padx=40, pady=20, bg='white',
    #                                  command=lambda: [self.create_enemy(), self.enemies_fall(), self.playMusic()])
    #     self.startButton.configure(width=10, activebackground="#33B5E5")
    #     self.startButton_window = self.myCanvas.create_window(395, 350, window=self.startButton)
    #
    #     self.endButton = tk.Button(self.mainWin, text='Quit', padx=40, pady=20, bg='white',
    #                                command=self.mainWin.destroy)
    #     self.endButton.configure(width=10, activebackground="#33B5E5")
    #     self.endButton_window = self.myCanvas.create_window(395, 450, window=self.endButton)


    def playMusic(self):
        winsound.PlaySound('sawsquarenoise_-_03_-_Towel_Defence_Ingame.wav', winsound.SND_LOOP + winsound.SND_ASYNC)

    def run(self):
        """This function runs the class, causing the program to run."""
        self.mainWin.mainloop()

    def create_enemy(self):
        self.enemyCount = self.enemyCount + 1
        x0 = random.randrange(0, 700)
        x1 = x0 + 50
        self.enemy = self.myCanvas.create_rectangle(x0, 0, x1, 50, fill="white")
        self.enemyList.append(self.enemy)
        if self.enemyCount != self.initialEnemyAmount:
            if self.winning == True:
                self.mainWin.after(self.timeApartEnemies, self.create_enemy)
    # def reset(self):
    #     self.winning = True
    #     self.myCanvas.delete('all')
    #     self.run()
    def enemies_fall(self):
        """Moves all the enemy shapes in the enemy List. If they go
      out of bounds they are taken off the canvas and taken off the list
      If not, they are moved down the canvas."""

        self.startButton.destroy()
        self.endButton.destroy()

        # take enemies off canvas and off list if they are out of range, otherwise move them
        for enum, enemy in enumerate(self.enemyList):
            coords = self.myCanvas.coords(enemy)
            if len(coords) > 1:
                if coords[3] >= 750:
                    self.enemyList.pop(enum)
                    self.myCanvas.delete(enemy)

                    self.loseLabel = tk.Label(self.mainWin, font='Times 20', text="You Lose!")
                    # self.loseLabel.grid(column=0, row=0)
                    self.loseLabel.configure(width=10, activebackground="#33B5E5")
                    self.loseLabel = self.myCanvas.create_window(395, 350, window=self.loseLabel)

                    self.winning = False

                    self.restartButton = tk.Button(self.mainWin, text='Restart?', padx=40, pady=20, bg='white',
                                                   command=self.restart())
                    self.restartButton.configure(width=10, activebackground="#33B5E5")
                    self.restartButton = self.myCanvas.create_window(395, 450, window=self.restartButton)

                    self.endButton = tk.Button(self.mainWin, text='Quit', padx=40, pady=20, bg='white',
                                               command=self.mainWin.destroy)
                    self.endButton.configure(width=10, activebackground="#33B5E5")
                    self.endButton_window = self.myCanvas.create_window(395, 550, window=self.endButton)

                else:
                    self.myCanvas.move(enemy, 0, 5)

            for bulletEnum, bullet in enumerate(self.bullets):  # deletes enemy if bullet in same position
                bulletCoords = self.myCanvas.coords(bullet.bullet)
                if coords[3] >= bulletCoords[3]:
                    if coords[0] <= bulletCoords[0] and coords[2] >= bulletCoords[2]:
                        self.enemiesRemaining = self.enemiesRemaining - 1

                        self.enemyList.pop(enum)
                        self.myCanvas.delete(enemy)

                        self.myCanvas.delete(bullet.bullet)
                        self.bullets.pop(bulletEnum)
                        self.hitCount = self.hitCount + 1

        # count enemies
        if self.bulletCount == 0:
            accuracyPercent = "-"
        else:
            accuracy = self.hitCount / self.bulletCount
            accuracy2 = round(accuracy, 2) * 100
            accuracy3 = int(accuracy2)
            accuracyPercent = f"{accuracy3} %"

        infoStr = (f"Level: {self.level}" + '\n' + '\n'
                                                   f"Enemies remaining: {str(self.enemiesRemaining)}" + '\n' + '\n'
                                                                                                               f"Accuracy: {accuracyPercent}")
        self.infoLabel = tk.Label(self.mainWin, font='Times', text=infoStr, fg='white')
        self.infoLabel["height"] = 34
        self.infoLabel["bg"] = "black"
        self.infoLabel["bd"] = 1
        self.infoLabel.grid(row=0, column=1, pady=1)

        if self.winning:
            # if self.level == 1:
            #     self.mainWin.after(10, self.enemies_fall)
            # if self.level == 2:
            #     self.mainWin.after(7, self.enemies_fall)
            # if self.level == 3:
            #     self.mainWin.after(5, self.enemies_fall)
            # if self.level == 4:
            #     self.mainWin.after(3, self.enemies_fall)
            self.mainWin.after(10, self.enemies_fall)

        # if self.winning == False:

        if self.enemiesRemaining == 0:
            if self.level != 4:
                self.initialEnemyAmount = self.initialEnemyAmount + 5
                self.enemiesRemaining = self.initialEnemyAmount
                # self.timeApartEnemies = self.timeApartEnemies - 350
                self.enemyCount = 0
                self.level = self.level + 1
                self.create_enemy()
            else:
                self.winLabel = tk.Label(self.mainWin, font='Times 20', text="You Win!")
                self.winLabel.grid(column=0, row=0)
                self.winning = False

    def go_left(self, event):
        x0, y0, x1, y1 = self.myCanvas.coords(self.r1)
        if x0 > 0:
            self.myCanvas.move(self.r1, -20, 0)

    def go_right(self, event):
        x0, y0, x1, y1 = self.myCanvas.coords(self.r1)
        if x1 < 750:
            self.myCanvas.move(self.r1, 20, 0)

    def space_key(self, event=0):
        x0, y0, x1, y1 = self.myCanvas.coords(self.r1)
        self.bullets.append(Bullet(self.myCanvas, x0, y0, x1, y1, (0, -10)))
        self.bulletCount = self.bulletCount + 1

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
