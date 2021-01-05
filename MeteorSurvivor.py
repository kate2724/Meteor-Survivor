# Names: Katelyn Breen, Gloriah Omwanda, Tatiana Jimenez-Thompson
# Course: COMP 12
# Instructor: Getiria Onsongo

# Summary:
# This file contains almost all of the code for the game. It contains two classes. The first one creates a bullet and
# moves it up the canvas. The second class creates the window for the game and the canvas. On that canvas, it draws the
# user, a white square at the bottom of the screen which the player can control. it also draws red squares at the top
# of the screen and moves them down the screen. The player uses the white square to shoot upwards at the red squares,
# which will cause both the bullet and the red square to disappear if properly aimed. If the player does not destroy
# all the red squares before they reach the other side of the screen, they will lose. If they go through all the levels
# and destroy all the red squares, they win the game.

# The other file we have is a music file. We cannot put our names and info in that file without causing it to not work.

# ------------------ imports ----------------
import tkinter as tk
import random
import winsound

# ------------------ GUI class and methods ----------------

class Bullet:
    """ Creates a bullet"""
    def __init__(self, canvas, x0, y0, x1, y1, movement):
        """ Takes in the inputs of a canvas, four numbers representing the user's location, and a number representing
        the amount of pixels the ship must move. creates a bullet at the given coordinates on the given canvas. sets
        the given movement to self.movement"""
        xavg = (x0 + x1) / 2 # calculates where the center of the user controlled square is
        self.bullet = canvas.create_line(xavg, y0, xavg, y1, fill='white', arrow=tk.FIRST) # creates bullet at the
        # center of the ship
        self.movement = movement

    def move(self, canvas):
        """moves the bullet by self.movement"""
        canvas.move(self.bullet, self.movement[0], self.movement[1]) # moves the bullet up the canvas


class MeteorSurvivor:
    """Creates a canvas, and draws a square on it that the user can control. Makes it so red squares fall from the
    top of the screen that the user must shoot. Add another level every time the user shoots all the red squares, up to
    four levels. Display a restart and quit button every thime the game ends."""

    def __init__(self):
        """Creates window and Canvas widget. Creates initial accumulator values and lists. Creates start and quit buttons
        on the canvas. Creates user controlled object at bottom of canvas. Binds key to movement and shooting."""
        self.mainWin = tk.Tk()
        self.mainWin.title("Meteor Survivor")

        # creates canvas that is 750 x 750 pixels, with a black background
        self.myCanvas = tk.Canvas(self.mainWin)
        self.myCanvas["width"] = 750
        self.myCanvas["height"] = 750
        self.myCanvas["bg"] = "black"
        self.myCanvas.grid(row=0, column=0)

        # initializes values used in later functions
        self.enemyCount = 0

        # used to calculate accuracy
        self.bulletCount = 0
        self.hitCount = 0

        self.level = 1
        self.initialEnemyAmount = 10 # initial amount of enemies/ meteors at level one, changes as user advances levels
        self.enemiesRemaining = self.initialEnemyAmount
        self.timeApartEnemies = 1250
        self.winning = True  # indicates that the player has not lost yet

        self.bullets = []  # store bullets that the player fires
        self.enemyList = []  # store enemies/ meteors

        self.tick_loop()  # start the tick loop function, which moves the bullets up the canvas, and takes them off if
        # they go out of range

        # Start button, calls create_enemy, enemies_fall, and playMusic.
        self.startButton = tk.Button(self.mainWin, text='Click to Start', padx=40, pady=20, bg='white',
                                     command=lambda: [self.create_enemy(), self.enemies_fall(), self.playMusic()])
        self.startButton.configure(width=10, activebackground="#33B5E5")
        self.startButton_window = self.myCanvas.create_window(395, 450, window=self.startButton)

        # quit button
        self.endButton = tk.Button(self.mainWin, text='Quit', padx=40, pady=20, bg='white',
                                   command=self.mainWin.destroy)
        self.endButton.configure(width=10, activebackground="#33B5E5")
        self.endButton_window = self.myCanvas.create_window(395, 550, window=self.endButton)

        self.titleLabel = tk.Label(self.mainWin, text=" Meteor Survivor ", font="Times 30 bold", bg='black', fg='red', bd=5, relief='raised')
        self.titleLabel_window = self.myCanvas.create_window(395, 100, window=self.titleLabel)

        self.instructions = tk.Label(self.mainWin, text= """Meteors are falling towards the earth, and YOU, random MAC student, 
        are our last hope for saving humanity. No pressure tho ;)
        \n TO PLAY: \n Press A or <-- to move left and Press D or --> to move right \n Press the space bar to shoot at meteors. 
        \n Last four levels. Destroy ALL meteors.""",
font='Arial 12 bold',  bg = 'black', fg='white', width=70)
        self.instructions_window = self.myCanvas.create_window(395, 275, window=self.instructions)

        # creates a rectangle on the canvas with its top left corner at position (375,700) and its bottom right corner
        # at position (425,750). The user can control this rectangle
        self.playerShip = self.myCanvas.create_rectangle(375, 700, 425, 750, fill="white")

        # binds the a, d, left, right, and space keys to the function, and calls their respective callback functions
        self.mainWin.bind("<Left>", self.go_left)
        self.mainWin.bind("<Right>", self.go_right)
        self.mainWin.bind("<a>", self.go_left)
        self.mainWin.bind("<d>", self.go_right)
        self.mainWin.bind("<space>", self.shoot)

    def run(self):
        """This function runs the class, causing the program to run."""
        self.mainWin.mainloop()
    def tick_loop(self):
        """removes bullets that go out of the range of the canvas from the list of bullets and from the canvas. if
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

    def playMusic(self):
        """Plays music when called"""
        winsound.PlaySound("meteorSurvivorMusic", winsound.SND_LOOP + winsound.SND_ASYNC)

    def create_enemy(self):
        """creates a enemy on the top of the canvas and adds it to a list of enemies. If there are still enemies left
        in the level and the user has not lost, creates another enemy after a certain amount of time."""
        self.enemyCount = self.enemyCount + 1
        x0 = random.randrange(0, 700) # randomly picks a place to drop the enemy from
        x1 = x0 + 50
        self.enemy = self.myCanvas.create_rectangle(x0, 0, x1, 50, fill="red")
        self.enemyList.append(self.enemy)
        if self.enemyCount != self.initialEnemyAmount:
            if self.winning == True:
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

        self.instructions.destroy()
        self.titleLabel.destroy()
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
            accuracyPercent = "-" # This is so a divide by 0 error does not appear
        else:
            accuracy = self.hitCount / self.bulletCount
            accuracy2 = round(accuracy, 2) * 100
            accuracy3 = int(accuracy2)
            accuracyPercent = f"{accuracy3} %"

        # create string with all of the information for the label next to the canvas
        # (level, remaining enemies, and accuracy)
        infoStr = (f"Level: {self.level}" + '\n' + '\n'
                            f"Meteors Remaining: {str(self.enemiesRemaining)}" + '\n' + '\n'
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
                self.winLabel = tk.Label(self.mainWin, font='Times 20', text="Congratulations! The earth has been saved!",
                                         bg='black', fg='white')
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

    def endgame(self):
        """after the user has lost, Creates label that says "You Lose!" and a restart and quit button. This restart
        button calls the self.reset function"""
        self.loseLabel = tk.Label(self.mainWin, font='Times 20', text="The earth has been destroyed!", bg='black', fg='white')
        self.loseLabel = self.myCanvas.create_window(395, 350, window=self.loseLabel)

        self.restartButton = tk.Button(self.mainWin, text='Restart?', padx=40, pady=20, bg='white',
                                       command=self.reset)
        self.restartButton.configure(width=10, activebackground="#33B5E5")
        self.restartButton = self.myCanvas.create_window(395, 450, window=self.restartButton)

        self.quitButton = tk.Button(self.mainWin, text='Quit', padx=40, pady=20, bg='white',
                                   command=self.mainWin.destroy)
        self.quitButton.configure(width=10, activebackground="#33B5E5")
        self.quitButton_window = self.myCanvas.create_window(395, 550, window=self.quitButton)

    def reset(self):
        """deletes everything on the canvas and resets all values seen in the __init__ function
        (accumulator values, lists, booleans). Calls self.enemies_fall and self.create_enemy again."""
        self.myCanvas.delete('all')

        self.playerShip = self.myCanvas.create_rectangle(375, 700, 425, 750, fill="white")

        self.enemyCount = 0
        self.bulletCount = 0
        self.hitCount = 0

        self.level = 1
        self.initialEnemyAmount = 10
        self.enemiesRemaining = self.initialEnemyAmount
        self.winning = True

        self.bullets = []
        self.enemyList = []

        self.enemies_fall()
        self.create_enemy()

    def go_left(self, event):
        """If the "a" key or "left" button are pressed, move the user controlled object left, if it is within certain
        bounds."""
        x0, y0, x1, y1 = self.myCanvas.coords(self.playerShip)
        if x0 > 0:
            self.myCanvas.move(self.playerShip, -20, 0)

    def go_right(self, event):
        """If the "d" key or "right" button are pressed, move the user controlled object right, if it is within certain
        bounds."""
        x0, y0, x1, y1 = self.myCanvas.coords(self.playerShip)
        if x1 < 750:
            self.myCanvas.move(self.playerShip, 20, 0)

    def shoot(self, event=0):
        """If the space key is pressed, append a bullet shape to a list of bullets."""
        x0, y0, x1, y1 = self.myCanvas.coords(self.playerShip)
        self.bullets.append(Bullet(self.myCanvas, x0, y0, x1, y1, (0, -10)))
        self.bulletCount = self.bulletCount + 1


# ------------------ Main program ----------------------

myGui = MeteorSurvivor()
myGui.run()
