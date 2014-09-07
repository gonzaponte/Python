from visual import *
from math import *

g   = 9.81

l0 = 1. 
l  = [ l0 - i*l0/20. for i in range(10)]
t0 = 20*pi/360.
x0 = [ li*sin(t0) for li in l ]
y0 = [ -li*cos(t0) for li in l ]
z0 = 1.

p = []
[sphere( pos=( 0., 0., z0 + float(i) ), p = vector(.0,.0,.0), radius = 0.25, color = color.red, make_trail=True, interval=10) for i in range(10) ]
for i in range(10):
    p += [sphere( pos=( x0[i], y0[i],z0+float(i)), p = vector(.0,.0,.0), radius = 0.25, color = color.blue, make_trail=True, interval=10)]

dt  = 1e-3

while True:
    rate(200)
    theta = [atan(-p[i].y/p[i].x) for i in range(10)]
    if theta[0]/p[0].x<0:
        print 'yes'
    F = [g/l[i]*sin(theta[i])*vector( p[i].y, -p[i].x, 0.) for i in range(10)]
    for i in range(10):
        p[i].p = p[i].p + F[i]*dt
        p[i].pos += p[i].p*dt

