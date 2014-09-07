from __future__ import division
from visual import *
from visual.graph import *
from math import *

def makespring( x, dx, y0, y1, N = 18, z = 0 ):
    dy = ( y1 - y0 ) / N
    return [ (x,y0,z) ] + [ ( x - (2*(i%2)-1)*dx, y0 + dy*i, z ) for i in range(1,N) ] + [ (x,y1,z) ]

pos0   = ( 0, 0, 0 )
p0     = vector( 0, 0, 0 )
m0     = 1.5
g      = 9.81
dt     = 0.01

k      = 2.
L      = 10
roz    = 0.1

red    = color.red
yellow = color.yellow
blue   = color.blue

line   = curve( pos = [(-1,0,0),(1,0,0)], radius = 0.1, color = yellow )
spring = curve( pos = makespring(0,.5,10,0), radius = 0.05, color = blue )
ball   = sphere( pos = pos0, radius = 0.5, color = red, mass = m0, p = p0 )

while True:
    rate(200)
    dx = -ball.y
#    print ball.y
    F = ball.mass * g - k * dx + roz * ball.p[1] / ball.mass
#    print F
    F = vector( 0, -F, 0 )
    ball.p   += F * dt
    ball.pos += ball.p * dt / ball.mass
    spring.pos = makespring(0,.5,10, ball.y)

