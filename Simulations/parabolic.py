from __future__ import division
from visual import *
from math import *

x0     = (  0, 10, 0 )
v0     = ( 10, 50, 0 )
xaxis  = (  1,  0, 0 )
yaxis  = (  0,  1, 0 )
zaxis  = (  0,  0, 1 )

mass   = 8.00
g      = 9.81
dt     = 5e-3
r0     = 5.00
p0     = vector( v0 ) * mass
F0     = - mass * g * vector(yaxis)

red     = color.red
yellow  = color.yellow
blue    = color.blue
orange  = color.orange
magenta = color.magenta

scene = display( title = 'Pendulo simple', x=0, y=0, width=1000, height=1000, center = (20,0,0), range = 200 )
scene.autoscale = False
scene.forward   = ( 0, 0, -1 )


ball  = sphere( pos = x0, radius = r0, mass       = mass, p = p0         , make_trail = True, color = red     )
veloc = arrow ( pos = x0, axis   = v0, shaftwidth = 0.3 , headwidth = 0.5, headlength = 1.0 , color = orange  )
accel = arrow ( pos = x0, axis   = F0, shaftwidth = 0.2 , headwidth = 0.5, headlength = 1.0 , color = magenta )


while ball.y > 0.:
    rate(200)
    ball.p    += F0 * dt
    ball.pos  += ball.p * dt / ball.mass
    veloc.pos  = ball.pos
    veloc.axis = ball.p / ball.mass
    accel.pos  = ball.pos

# if balla.y > 5:
#     balla.mass *= 1.01
# if ballb.y > 5:
#     ballb.mass *= 1.01
