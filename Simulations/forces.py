from visual import *
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

def force3(cte,p1,p2):
    return -cte*dr(p1,p2)/r(p1,p2)**3

def force4(cte,p1,p2):
    return -cte*dr(p1,p2)/r(p1,p2)**4

def force5(cte,p1,p2):
    return -cte*dr(p1,p2)/r(p1,p2)**5

def force6(cte,p1,p2):
    return -cte*dr(p1,p2)/r(p1,p2)**6


def proba():
    dt    = 1e-17
    r     = 1e-9
    p03   = 5e5*0.511*m0
    p04   = 5e6*0.511*m0
    p05   = 5e7*0.511*m0
    p06   = 5e8*0.511*m0
    
    p  = sphere( pos=(0.0, 0.0, 0.0), radius=r0/5, color = color.red)
    e3 = sphere( pos=(0.0,   r, 0.0), radius = r0, color = color.blue  , make_trail=True )
    e4 = sphere( pos=(0.0,   r, 0.0), radius = r0, color = color.yellow, make_trail=True )
    e5 = sphere( pos=(0.0,   r, 0.0), radius = r0, color = color.orange, make_trail=True )
    e6 = sphere( pos=(0.0,   r, 0.0), radius = r0, color = color.green , make_trail=True )

    e3.mass = e4.mass = e5.mass = e6.mass = 0.511*m0
    e3.p = vector(0.0,p03,0.0)
    e4.p = vector(0.0,p04,0.0)
    e5.p = vector(0.0,p05,0.0)
    e6.p = vector(0.0,p06,0.0)
    
    while True:
        rate(200)
        F3 = force3(em,p,e3)
        F4 = force3(em,p,e4)
        F5 = force3(em,p,e5)
        F6 = force3(em,p,e6)
        e3.p = e3.p - F3*dt
        e4.p = e4.p - F4*dt
        e5.p = e5.p - F5*dt
        e6.p = e6.p - F6*dt
        e3.pos = e3.pos + e3.p/e3.mass*dt
        e4.pos = e4.pos + e4.p/e4.mass*dt
        e5.pos = e5.pos + e5.p/e5.mass*dt
        e6.pos = e6.pos + e6.p/e6.mass*dt


proba()

