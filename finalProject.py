import turtle
import time

def enter(turtle):
    turtle.penup()
    turtle.right(90)
    turtle.forward(30)
    turtle.left(90)
    turtle.pendown()


def introScreen():
    string = "Spacebar to shoot. "
    string2 = "A and D to move left and right."
    string3 = "Kill all enemies. Last 10 levels."

    wn = turtle.Screen()
    wn.bgcolor("black")

    jan = turtle.Turtle()
    jan.hideturtle()
    jan.goto(-150, 0)
    jan.color("white")

    jan.write(string, font=("Papyrus", 17, "normal"))
    enter(jan)
    jan.write(string2, font=("Papyrus", 17, "normal"))
    enter(jan)
    jan.write(string3, font=("Papyrus", 17, "normal"))
    time.sleep(3)
    jan.clear()


def drawLsystem(aTurtle, turt2, instructions):
    for cmd in instructions:
        if cmd == 'a':
            aTurtle.forward(30)
        elif cmd == 'd':
            aTurtle.backward(30)
        elif cmd == " ":
            turt2.hideturtle()
            pos = user.position()
            turt2.goto(pos)
            turt2.showturtle()
            turt2.forward(500)

def shoot(turt):
    pos = user.position()


introScreen()

# create user
user = turtle.Turtle()
user.color("white")
user.penup()
user.left(180)
user.shape("square")

bullet = turtle.Turtle()
bullet.color("white")
bullet.penup()
bullet.shape("arrow")
bullet.left(90)
while True:
    inp = input("move: ")
    drawLsystem(user, bullet, inp)

