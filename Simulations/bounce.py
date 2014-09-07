from visual import *
from math import *

theta0 = 30*pi/360.
phi0   = 25*pi/360.
dt     = 5e-3
L      = 10.
v0     = 50
B = box( pos=(0.,0.,0.), length=2*L, height=2*L, width=2*L, opacity=0.2)

B.color = color.green

S = sphere( pos=(0.,0.,0.), radius = L/15., p = vector(sin(theta0)*cos(phi0),
                                                       sin(theta0)*sin(phi0),
                                                       cos(theta0)))

S.p *= v0
S.color = color.orange

while True:
    rate(100)
    
    if abs( S.x ) >  L - S.radius:
        S.p.x *= -1
    if abs( S.y ) >  L - S.radius:
        S.p.y *= -1
    if abs( S.z ) >  L - S.radius:
        S.p.z *= -1
    
    
    S.pos += S.p*dt
