from __future__ import division
from visual import *
from visual.graph import *
from math import *

pos0   = ( 0, 10, 0 )
p0     = vector(1,0,0)
m0     = 1.5
g      = 9.81
dt     = 0.01
delta  = 0.8
roz    = 0.1

red    = color.red
yellow = color.yellow
blue   = color.blue

scene = display( title = 'Boing', x=0, y=0, width=600, height=600, center = (0,5,0) )
scene.autoscale = False
scene.forward   = ( 0, 0, -1 )


ball   = sphere( pos = pos0, radius = 0.5, color = red, mass = m0, p = p0, make_trail = True )
line   = curve ( pos = [(0,0,0),(30,0,0)], radius = 0.1, color = yellow )

while True:
    rate(200)
    scene.center[0] = ball.pos[0]
    F = ball.mass * g + roz * ball.p[1] / ball.mass
    F = vector( 0, -F, 0 )
    ball.p += F * dt
    ball.pos += ball.p * dt / ball.mass
    if ball.y <= 0.5:
        ball.p[1] *= -1
        delta **= 1.01


