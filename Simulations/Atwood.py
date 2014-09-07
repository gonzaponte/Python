from __future__ import division
from visual import *
from visual.graph import *
from math import *

r0     = .25
xaxis  = ( 1,0,0)
yaxis  = ( 0,1,0)
zaxis  = ( 0,0,1)

posa0  = (-1, 0,0)
posb0  = (+1, 0,0)
posp0  = ( 0,10,0)

pa0    = vector(0,0,0)
pb0    = vector(0,0,0)

posap  = (-1,10,0)
posbp  = (+1,10,0)

cha    = [ posa0, posap ]
chb    = [ posbp, posb0 ]

massa  = 1.00
massb  = 1.20
g      = 9.81
dt     = 0.01

red    = color.red
yellow = color.yellow
blue   = color.blue

puley  = ring  ( pos = posp0, radius = 1.00, color = yellow, axis = zaxis          )
balla  = sphere( pos = posa0, radius = r0  , color = red   , mass = massa, p = pa0 )
ballb  = sphere( pos = posb0, radius = r0  , color = red   , mass = massb, p = pb0 )
chaina = curve ( pos = cha  , radius = 0.05, color = blue  )
chainb = curve ( pos = chb  , radius = 0.05, color = blue  )

while (balla.pos-puley.pos).mag > 1.2 and (ballb.pos-puley.pos).mag > 1.2:
    rate(200)
    Fa = balla.mass * g
    Fb = ballb.mass * g
    F  = vector( 0, Fa - Fb, 0 )
    balla.p   -=  F * dt
    ballb.p   +=  F * dt
    balla.pos += balla.p * dt / balla.mass
    ballb.pos += ballb.p * dt / ballb.mass
    
    chaina.pos = [ balla.pos, posap ]
    chainb.pos = [ ballb.pos, posbp ]

    # if balla.y > 5:
    #     balla.mass *= 1.01
    # if ballb.y > 5:
    #     ballb.mass *= 1.01
