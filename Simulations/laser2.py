from visual import *
from visual.graph import *
from math import *
from random import random
r = random

dt      = 5e-03  # temporal step
Pi      = 1e-6   # probability of creating new photons
Pe      = 1e-2   # probability of creating new photons
T       = 2e-3   # Probability of transfer photons

# Initial conditions
nphotons = 5
ninside  = 5
nemited  = 0

# Displays
Nphotons  = gcurve( color = color.orange )
gdisplay( x=0, y=0, width=800, height=400,title='Number of photons', xtitle='time', ytitle='# photons' )

intensity = gcurve( color = color.magenta )
gdisplay( x=0, y=400, width=800, height=400,title='Number of photons emited', xtitle='time', ytitle='# photons' )

t = 0
# Advance in time
while True:
    rate(100)

    if r()<Pi:
        nphotons += 1
        ninside  += 1
    
    # Create new photons
    for i in xrange( ninside ):
        if r()<Pe:
            nphotons += 1
            ninside  += 1

    # Delete leaving photons
    for i in xrange( ninside ):
        if r()<T:
            nemited += 1
            ninside -= 1

    t += dt
    Nphotons.plot ( pos = ( t, ninside/float(nphotons) ) )
    intensity.plot( pos = ( t, nemited/float(nphotons) ) )


