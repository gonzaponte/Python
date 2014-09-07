from visual import *
from visual.graph import *
from math import *

q0  = 1.602e-19
eps = 8.854e-12
c   = 299792458.
m0  = 1e6*q0/c**2
em  = q0**2./(4.*3.14159265*eps)
r0  = 5e-11
G   = 6.67e-11
g   = 9.81

def dr(p1,p2):
    return p1.pos - p2.pos

def r(p1,p2):
    return mag(dr(p1,p2))

def force(cte,p1,p2):
    return -cte*dr(p1,p2)/r(p1,p2)**3

def earthvenus():
    earth = []
    venus = []
    dt    = 1e-19
    re    = 1e-9
    rv    = 3e-10
    pe    = 2.25e6*0.511*m0
    pv    = -2.70e6*0.511*m0
    sun   = sphere( pos=( 0.0, 0.0, 0.0), radius = r0/15, color = color.yellow )
    earth = sphere( pos=( r0 , 0.0, 0.0), radius = r0/20, color = color.blue, make_trail = True )
    venus = sphere( pos=( 0.0,2*r0/3, 0.0), radius = r0/20, color = color.green, make_trail = True )
    earth.mass = venus.mass = 0.511*m0
    earth.p = pe*vector(0.0,1.0,0.0)
    venus.p = pv*vector(1.0,0.0,0.0)
    
    f1 = gcurve( color = color.orange )
    gdisplay()
    f2 = gcurve( color = color.magenta )
    t=0
    while True:
        rate(200)
        f1.plot( pos = ( t, (earth.pos - venus.pos).mag ) )
        f2.plot( pos = earth.pos - venus.pos )
        t += dt
        Fe = force( em, sun, earth)
        Fv = force( em, sun, venus)
        earth.p = earth.p - Fe*dt
        venus.p = venus.p - Fv*dt
        earth.pos = earth.pos + earth.p/earth.mass*dt
        venus.pos = venus.pos + venus.p/venus.mass*dt
        #print sqrt( earth.pos.x**2 + earth.pos.y**2 ), sqrt( venus.pos.x**2 + venus.pos.y**2 )

earthvenus()
