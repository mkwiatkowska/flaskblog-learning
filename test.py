import turtle
import math
bob = turtle.Turtle()


def square(t, l):
    for i in range(4):
        t.forward(l)
        t.left(90)


def polygon(t, l, n):
    for i in range(n):
        t.forward(l)
        t.left(360/n)


def circle(t, r):
    length = r * math.sin(15)
    polygon(t, length, int(360/15))


def sinus(t): #retarded
    for f in range(4):
        if f == 1 or f == 2:
            for i in range(90):
                t.forward(1)
                t.left(1)
        else:
            for i in range(90):
                t.forward(1)
                t.rt(1)

#square(bob, 10)
#polygon(bob, 20,13)
#circle(bob, 15)
#sinus(bob)

turtle.mainloop()