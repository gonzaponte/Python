from visual import *
from math import *
from sys import argv

g      = 9.81
L      = 10.
dt     = 5e-3
roz    = 1e-1
theta0 = 90 * pi / 180
pos0   = ( +L * sin(theta0), - L * cos(theta0), 0 )
F0     = ( -L * sin(theta0), - L * cos(theta0), 0 )
p0     = vector( 0, 0, 0 )
r0     = 0.25
mass   = 1.
chain  = [(0,0,0),pos0]

scene = display( title = 'Pendulo simple', x=0, y=0, width=800, height=800, center = (0,-L/2,0) )
scene.autoscale = False
scene.forward   = ( 0, 0, -1 )

chain = curve ( pos = chain, radius = 0.05, color = color.blue )
ball  = sphere( pos = pos0 , p = p0, radius = r0, color = color.red, mass = mass, make_trail = True )

try:
    argv[1]
    arrows = True
except:
    arrows = False

if arrows:
    velocity     = arrow( pos = ball.pos, axis = ball.p/ball.mass, shaftwidth = 0.2, headwidth = 0.5, headlength = 1.0, color = color.orange  )
    acceleration = arrow( pos = ball.pos, axis = F0              , shaftwidth = 0.2, headwidth = 0.5, headlength = 1.0, color = color.magenta )

while True:
    rate(200)
    theta     = atan(-ball.x/ball.y)
    T         = 3 * cos( theta ) - 2 * cos ( theta0 )
    F         = ball.mass * g * vector( - T * sin( theta ), T * cos( theta ) - 1 , 0 )
    ball.p   += F * dt
    ball.pos += ball.p / ball.mass * dt
    chain.pos = [(0,0,0),ball.pos]

    if arrows:
        velocity    .pos  = ball.pos
        velocity    .axis = ball.p / ball.mass
        acceleration.pos  = ball.pos
        acceleration.axis = F

