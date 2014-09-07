from __future__ import division
from visual import *
from visual.graph import *
from math import *

L      = 10
l      = L/2
Rpuley = 2.
rpuley = Rpuley/2
rball  = rpuley/8
rchain = rball/5

xaxis  = ( 1, 0, 0 )
yaxis  = ( 0, 1, 0 )
zaxis  = ( 0, 0, 1 )
zero   = ( 0, 0, 0 )

posa   = ( -2, 0, 0 )
posb   = ( +1, 0, 0 )
posc   = ( +3, 0, 0 )
posp1  = ( +0, L, 0 )
posp2  = ( +2, l, 0 )

hooka  = ( -2, L, 0 )
hookp  = ( +2, L, 0 )
hookb  = ( +1, l, 0 )
hookc  = ( +3, l, 0 )

chaina = [ posa , hooka ]
chainp = [ posp2, hookp ]
chainb = [ posb , hookb ]
chainc = [ posc , hookc ]

massa  = 2.20
massb  = 1.11
massc  = 1.10
g      = 9.81
dt     = 0.01

red    = color.red
yellow = color.yellow
blue   = color.blue

puley1 = ring  ( pos = posp1 , radius = Rpuley, color = yellow, axis = zaxis, p = vector(0,0,0) )
puley2 = ring  ( pos = posp2 , radius = rpuley, color = yellow, axis = zaxis, p = vector(0,0,0) )
balla  = sphere( pos = posa  , radius = rball , color = red   , mass = massa, p = vector(0,0,0) )
ballb  = sphere( pos = posb  , radius = rball , color = red   , mass = massb, p = vector(0,0,0) )
ballc  = sphere( pos = posc  , radius = rball , color = red   , mass = massc, p = vector(0,0,0) )
chaina = curve ( pos = chaina, radius = rchain, color = blue  )
chainp = curve ( pos = chainp, radius = rchain, color = blue  )
chainb = curve ( pos = chainb, radius = rchain, color = blue  )
chainc = curve ( pos = chainc, radius = rchain, color = blue  )

while ((balla .pos - puley1.pos).mag > 1.01 * ( Rpuley + rball  ) and
       (ballb .pos - puley2.pos).mag > 1.01 * ( rpuley + rball  ) and
       (ballc .pos - puley2.pos).mag > 1.01 * ( rpuley + rball  ) and
       (puley1.pos - puley2.pos).mag > 1.01 * ( Rpuley + rpuley ) ):
    
    rate(200)
    F  = g
    F /= 4 * ballb.mass * ballc.mass + balla.mass * ballb.mass +     balla.mass * ballc.mass
    Fa = 4 * ballb.mass * ballc.mass - balla.mass * ballb.mass -     balla.mass * ballc.mass; Fa *= balla.mass * F
    Fb = 3 * balla.mass * ballc.mass - balla.mass * ballb.mass - 4 * ballb.mass * ballc.mass; Fb *= ballb.mass * F
    Fc = 3 * balla.mass * ballb.mass - balla.mass * ballc.mass - 4 * ballb.mass * ballc.mass; Fc *= ballc.mass * F
    Fp = - 0.5 * ( Fb/ballb.mass + Fc/ballc.mass )
    Fp = -Fa
    
    Fa = vector( 0, Fa, 0 )
    Fp = vector( 0, Fp, 0 )
    Fb = vector( 0, Fb, 0 )
    Fc = vector( 0, Fc, 0 )
    
    balla .p   +=  Fa * dt
    ballb .p   +=  Fb * dt
    ballc .p   +=  Fc * dt
    puley2.p   +=  Fp * dt
    
    balla .pos += balla .p * dt / balla.mass
    ballb .pos += ballb .p * dt / ballb.mass
    ballc .pos += ballc .p * dt / ballc.mass
    puley2.pos += puley2.p * dt
    
    hookb  = ( +1, puley2.y, 0 )
    hookc  = ( +3, puley2.y, 0 )

    
    chaina.pos = [ balla .pos, hooka ]
    chainp.pos = [ puley2.pos, hookp ]
    chainb.pos = [ ballb .pos, hookb ]
    chainc.pos = [ ballc .pos, hookc ]
