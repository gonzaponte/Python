from check import *
from math import *
import swampy.TurtleWorld as tw

def maketurtle():
    ''' This is a function to establish the turtle and its properties.'''
    
    w = tw.TurtleWorld()
    t = tw.Turtle()
    w.minsize(1000,1000)
    t.set_color('orange')
    t.set_pen_color('purple')
    t.delay= 0.00001
    tw.pu(t)
    tw.lt(t)
    tw.bk(t,300)
    tw.rt(t)
    tw.pd(t)
    print '\n\nType quit() to exit.\n\n'
    return w,t

def regular(t,n):
    ''' This is a function to make any regular polygon with a turtle and the number of sides.'''
    if n<3 or not isint(n):
        wrong(regular)
    angle = 360./n
    step  = 100*angle*(2*pi/360)
    for i in range(n):
        t.fd(step)
        t.lt(angle)
    #t.die()

def square(t):
    regular(t,4)

def circle(t):
    regular(t,1000)
    #arc( t, 50, 360 )

def pentagon(t):
    regular(t,5)

def arc( t, r=10, theta=30 ):
    length = (2*pi/360)*r*theta
#    n = int(length/3) + 1
#    step = length / n
#    angle = float(theta) / n
    angle = 1
    n = theta/angle
    step = length/n
    for i in range(n):
        t.fd(length)
        t.lt(angle)

def petal( t, r=10, theta=30 ):
    for i in range(2):
        arc( t, r, theta )
        t.lt(180-theta)

def flower( t, n=6, r=10, theta=30):
    for i in range(1,n+1):
        petal(t,r,theta)
        t.lt(360/n)

def snowflake(t,step0=64,min=8):
    def side(step):
        if step==min:
            t.fd(step)
            t.rt(60)
            t.fd(step)
            t.lt(120)
            t.fd(step)
            t.rt(60)
            t.fd(step)
        elif step<min:
            sys.exit('Turtle step began lower than minimum step')
        else:
            step = step/2
            side(step)
            t.rt(60)
            side(step)
            t.lt(120)
            side(step)
            t.rt(60)
            side(step)
    
    if step0<min:
        wrong(snowflake)

    for i in range(3):
        side(step0/2)
        t.lt(120)

def spiral(t,r=0.01,N=1000):
    for i in range(N):
        arc(t,r,180)
        r *= 2

def spiral2(t,r=0.01,N=100000):
    for i in range(N):
        arc(t,r,1)
        r *= 1 + 1./N
