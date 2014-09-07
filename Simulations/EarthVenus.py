from visual import *
from visual.graph import *
from math import *

UA = 149597870700. # m
km = 1e3 # m

G   = 6.67384e-11
dt = 3600*6.

Msun     = 1.9890e30
Mvenus   = 4.8670e24
Mearth   = 5.9720e24

Rvenus   = 0.723332 * UA
Rearth   = 1.000000 * UA

rsun     = 696342 * km * 10
rvenus   = 6052   * km * 1000
rearth   = 6371   * km * 1000

Vvenus   = 35.0214 * km
Vearth   = 29.7800 * km

def dr(p1,p2):
    return p1.pos - p2.pos

def r(p1,p2):
    return mag(dr(p1,p2))

def force(cte,p1,p2):
    return -cte*dr(p1,p2)/r(p1,p2)**3


sun   = sphere( pos=( 0.0, 0.0, 0.0), radius = rsun, color = color.yellow )
earth = sphere( pos=( Rearth , 0.0, 0.0), radius = rearth, color = color.blue   , make_trail = True )
venus = sphere( pos=( 0.0, Rvenus , 0.0), radius = rvenus, color = color.green  , make_trail = True )
earth.mass = Mearth
venus.mass = Mvenus
sun.mass   = Msun
earth.p = Mearth * Vearth * vector(  0.0, 1.0, 0.0 )
venus.p = Mvenus * Vvenus * vector( -1.0, 0.0, 0.0 )

f1 = gcurve( color = color.orange )
gdisplay()
f2 = gcurve( color = color.magenta )
t=0

while True:
    rate(200)
    f1.plot( pos = ( t, (earth.pos - venus.pos).mag ) )
    f2.plot( pos = ( earth.pos - venus.pos )/UA )
    t += dt
    Fe = force( G*Msun*Mearth, sun, earth)
    Fv = force( G*Msun*Mvenus, sun, venus)
    earth.p = earth.p - Fe*dt
    venus.p = venus.p - Fv*dt
    earth.pos = earth.pos + earth.p/earth.mass*dt
    venus.pos = venus.pos + venus.p/venus.mass*dt




















