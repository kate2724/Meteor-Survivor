import tkinter as tk
import random
import winsound
from tkinter import NW

import arcade
from PIL import Image, ImageTk


# ------------------ GUI class and methods ----------------

class Bullet:
    def __init__(self, canvas, x0, y0, x1, y1, movement):
        """creates a bullet at the given coordinates on the given canvas. sets the given movement to self.movement"""
        xavg = (x0 + x1) / 2
        self.bullet = canvas.create_line(xavg, y0, xavg, y1, fill='white', arrow=tk.FIRST)
        self.movement = movement

    def move(self, canvas):
        """moves the bullet by self.movement"""
        canvas.move(self.bullet, self.movement[0], self.movement[1])


class BasicGui:
    """Creates a canvas, and draws a square on it that the user can control"""

    def __init__(self):
        """Creates window and Canvas widget. Creates initial accumulator values and lists. Creates start and quit buttons
        on the canvas. Creates user controlled object at bottom of canvas. Binds key to movement and shooting."""
        self.mainWin = tk.Tk()
        self.mainWin.title("Block Survivor")

        # creates canvas that is 750 x 750 pixels, with a black background
        self.myCanvas = tk.Canvas(self.mainWin)
        self.myCanvas["width"] = 750
        self.myCanvas["height"] = 750
        self.myCanvas["bg"] = "black"
        self.myCanvas.grid(row=0, column=0)

        # initializes values used in later functions
        self.enemyCount = 0
        self.bulletCount = 0
        self.hitCount = 0
        self.iteration = 1

        self.level = 1  # initializes game level
        self.initialEnemyAmount = 10
        self.enemiesRemaining = self.initialEnemyAmount
        self.timeApartEnemies = 1250
        self.winning = True

        self.bullets = []  # store bullets
        self.enemyList = []  # store enemies

        self.tick_loop()  # start the tick loop

        # Start button, calls create_enemy, enemies_fall, and playMusic.
        self.startButton = tk.Button(self.mainWin, text='Click to Start', padx=40, pady=20, bg='white',
                                     command=lambda: [self.create_enemy(), self.enemies_fall(), self.playMusic()])
        self.startButton.configure(width=10, activebackground="#33B5E5")
        self.startButton_window = self.myCanvas.create_window(395, 350, window=self.startButton)

        # quit button
        self.endButton = tk.Button(self.mainWin, text='Quit', padx=40, pady=20, bg='white',
                                   command=self.mainWin.destroy)
        self.endButton.configure(width=10, activebackground="#33B5E5")
        self.endButton_window = self.myCanvas.create_window(395, 450, window=self.endButton)

        # creates a rectangle on the canvas with its top left corner at position (475,750) and its bottom right corner
        # at position (525,800)
        img = ImageTk.PhotoImage(Image.open('fighter.png'))
        self.myCanvas.create_image(375,375, anchor=NW , image=img)
        # load = Image.open("fighter.png")
        # render = ImageTk.PhotoImage(load)
        # self.img = tk.Label(self.mainWin, image=render)
        # self.img.image = render
        # self.img.place(x=375, y=725)

        # binds the a, d, left, right, and space keys to the function, and calls their respective callback functions
        self.mainWin.bind("<Left>", self.go_left)
        self.mainWin.bind("<Right>", self.go_right)
        self.mainWin.bind("<a>", self.go_left)
        self.mainWin.bind("<d>", self.go_right)
        self.mainWin.bind("<space>", self.space_key)

    def playMusic(self):
        """Plays music when called"""
        winsound.PlaySound('gameMusic.wav', winsound.SND_LOOP + winsound.SND_ASYNC)

    def run(self):
        """This function runs the class, causing the program to run."""
        self.mainWin.mainloop()

    def endgame(self):
        """Creates label that says "You Lose!" and a restart and quit button."""
        self.loseLabel = tk.Label(self.mainWin, font='Times 20', text="You Lose!")
        self.loseLabel.configure(width=10, activebackground="#33B5E5")
        self.loseLabel = self.myCanvas.create_window(395, 350, window=self.loseLabel)

        self.restartButton = tk.Button(self.mainWin, text='Restart?', padx=40, pady=20, bg='white',
                                       command=self.reset)
        self.restartButton.configure(width=10, activebackground="#33B5E5")
        self.restartButton = self.myCanvas.create_window(395, 450, window=self.restartButton)

        self.endButton = tk.Button(self.mainWin, text='Quit', padx=40, pady=20, bg='white',
                                   command=self.mainWin.destroy)
        self.endButton.configure(width=10, activebackground="#33B5E5")
        self.endButton_window = self.myCanvas.create_window(395, 550, window=self.endButton)

    def reset(self):
        """deletes everything on the canvas and resets all values (accumulator values, lists, booleans). Calls
        self.enemies_fall and self.create_enemy again."""
        self.myCanvas.delete('all')

        self.r1 = self.myCanvas.create_rectangle(375, 700, 425, 750, fill="white")

        self.enemyCount = 0
        self.bulletCount = 0
        self.hitCount = 0
        self.iteration = self.iteration + 1

        self.level = 1  # initializes game level
        self.initialEnemyAmount = 10
        self.enemiesRemaining = self.initialEnemyAmount
        self.timeApartEnemies = 1500
        self.winning = True

        self.bullets = []  # store bullets
        self.enemyList = []  # store enemies

        self.enemies_fall()
        self.create_enemy()

    def create_enemy(self):
        """creates a enemy on the top of the canvas and adds it to a list of enemies. If there are still enemies left
        in the level and the user has not lost, creates another enemy after a certain amount of time."""
        self.enemyCount = self.enemyCount + 1
        x0 = random.randrange(0, 700)
        x1 = x0 + 50
        self.enemy = self.myCanvas.create_rectangle(x0, 0, x1, 50, fill="white")
        self.enemyList.append(self.enemy)
        if self.enemyCount != self.initialEnemyAmount:
            if self.winning == True:
                # if self.iteration == 1:
                self.mainWin.after(self.timeApartEnemies, self.create_enemy)

    def enemies_fall(self):
        """Moves all the enemy shapes in the enemy List down. If they go
      out of bounds they are taken off the canvas and taken off the list. If this happens, the user
      has lost the game, and the function that keeps moving things will not be recalled, stopping the game. This function
      will then call the function endgame().

      If the enemies have not gone out of bounds, they are moved down the canvas.

      If the bullet is in the same position as the enemy, that enemy will be taken off the canvas and the list.
      The bullet will also be taken off the canvas and its list.

      A label to the right of the canvas will list of certain info like enemies left, level, and accuracy.

      When the amount of enemies remaining in a level equals zero, if it is not yet the final level, the function
      create_enemy is called, the level is increased, and the amount of initial enemies is increased. The speed at which
      the enemies fall is also increased.

      If there are no enemies left, and it is the final level, a label saying "You Win!" is put on the canvas, along
      with a restart button and a quit button."""

        self.startButton.destroy()
        self.endButton.destroy()

        # take enemies off canvas and off list if they are out of range, set winning to false and call endgame,
        # otherwise move enemies down screen.
        for enum, enemy in enumerate(self.enemyList):
            coords = self.myCanvas.coords(enemy)
            if len(coords) > 1:
                if coords[3] >= 750:
                    self.enemyList.pop(enum)
                    self.myCanvas.delete(enemy)

                    self.winning = False

                    self.mainWin.after(1250, self.endgame())
                else:
                    self.myCanvas.move(enemy, 0, 10)

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


        # calculate accuracy
        if self.bulletCount == 0:
            accuracyPercent = "-"
        else:
            accuracy = self.hitCount / self.bulletCount
            accuracy2 = round(accuracy, 2) * 100
            accuracy3 = int(accuracy2)
            accuracyPercent = f"{accuracy3} %"

        # create string with all of the information for the label next to the canvas
        # (level, remaining enemies, and accuracy)
        infoStr = (f"Level: {self.level}" + '\n' + '\n'
                            f"Enemies remaining: {str(self.enemiesRemaining)}" + '\n' + '\n'
                            f"Accuracy: {accuracyPercent}")

        # create label next to canvas with statistics about the game
        self.infoLabel = tk.Label(self.mainWin, font='Times 18', text=infoStr, fg='white')
        self.infoLabel["height"] = 27
        self.infoLabel["bg"] = "black"
        self.infoLabel["bd"] = 9
        self.infoLabel.grid(row=0, column=1, pady=1)


        # recalls the function enemies_fall at different speeds depending on the level
        if self.winning:
            if self.level == 1:
                self.mainWin.after(33, self.enemies_fall)
            if self.level == 2:
                self.mainWin.after(27, self.enemies_fall)
            if self.level == 3:
                self.mainWin.after(23, self.enemies_fall)
            if self.level == 4:
                self.mainWin.after(20, self.enemies_fall)

        # if there are no enemies left in the level and it's not the final level, reset values, and recall create_enemy
        if self.enemiesRemaining == 0:
            if self.level != 4:
                self.initialEnemyAmount = self.initialEnemyAmount + 5
                self.enemiesRemaining = self.initialEnemyAmount
                self.enemyCount = 0
                self.level = self.level + 1
                self.create_enemy()

            # if it is the last level and there are no enemies left, create "you win!" label, restart button, and quit
            # button.
            else:
                self.winLabel = tk.Label(self.mainWin, font='Times 20', text="You Win!")
                self.winLabel.configure(width=10, activebackground="#33B5E5")
                self.winLabel_window = self.myCanvas.create_window(395, 350, window=self.winLabel)

                self.restartButton = tk.Button(self.mainWin, text='Restart?', padx=40, pady=20, bg='white',
                                               command=self.reset)
                self.restartButton.configure(width=10, activebackground="#33B5E5")
                self.restartButton = self.myCanvas.create_window(395, 450, window=self.restartButton)

                self.endButton = tk.Button(self.mainWin, text='Quit', padx=40, pady=20, bg='white',
                                           command=self.mainWin.destroy)
                self.endButton.configure(width=10, activebackground="#33B5E5")
                self.endButton_window = self.myCanvas.create_window(395, 550, window=self.endButton)

                self.winning = False

    def go_left(self, event):
        """If the "a" key or "left" button are pressed, move the user controlled object left, if it is within certain
        bounds."""
        x0, y0, x1, y1 = self.myCanvas.coords(self.r1)
        if x0 > 0:
            self.myCanvas.move(self.r1, -20, 0)

    def go_right(self, event):
        """If the "d" key or "right" button are pressed, move the user controlled object right, if it is within certain
        bounds."""
        x0, y0, x1, y1 = self.myCanvas.coords(self.r1)
        if x1 < 750:
            self.myCanvas.move(self.r1, 20, 0)

    def space_key(self, event=0):
        """If the space key is pressed, append a bullet shape to a list of bullets."""
        x0, y0, x1, y1 = self.myCanvas.coords(self.r1)
        self.bullets.append(Bullet(self.myCanvas, x0, y0, x1, y1, (0, -10)))
        self.bulletCount = self.bulletCount + 1

    def tick_loop(self):
        """removes bullets that travel out of a certain bounds from the list of bullets and from the canvas. if
        they are not out of range, move them up the canvas."""
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
