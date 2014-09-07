from visual import *
from visual.graph import *
from ROOT import TRandom3
from math import *
from General import *

R  = TRandom3()
R.SetSeed(0)
U  = R.Uniform
V  = lambda A: A * ( 2. * U() - 1. )
N  = 5
dt = 5e-3
x0 = 100.
v0 = 100.
tau = 80.
scene = display( title = 'LHCb collision', x=0, y=0, width=1200, height=675, center=(0,0,0.) )


p1 = sphere( pos    = ( -x0, 0., 0. ),
            radius = 0.8,
            color  = color.red,
            p      = +v0 * vector( 1., 0., 0. ),
            make_trail = True )

p2 = sphere( pos    = ( +x0, 0., 0. ),
            radius = 0.8,
            color  = color.red,
            p      = -v0 * vector( 1., 0., 0. ),
            make_trail = True )

while (p2.pos - p1.pos).mag > 1e-3:
    rate(200)
    p1.pos = p1.pos + p1.p * dt
    p2.pos = p2.pos + p2.p * dt

p1.visible = False
p2.visible = False
del p1
del p2

v = 10.
ps = [sphere( pos    = ( 0., 0., 0. ),
            radius = 0.1,
            color  = color.green,
            p      = v * vector( V(1), V(1), 0. ),
            make_trail = True ) for i in range(N) ]

P = reduce( lambda x,y: x+y, [ p.p for p in ps ] )
for p in ps:
    p.p -= P/N

t = 0
while t < tau:
    rate(200)
    t += 1
    for p in ps:
        p.pos = p.pos + p.p * dt

pos3 = ps[3].pos
p3   = ps[3].p
ps[3].visible = False
del ps[3]

ps2 = [sphere( pos = pos3,
       radius = 0.1,
       color  = color.blue,
       p      = v * vector( V(1), V(1), 0. ),
       make_trail = True ) for i in range(N) ]

P = reduce( lambda x,y: x+y, [ p.p for p in ps2 ] )
for p in ps2:
    p.p += p3 - P/N

ps += ps2

while True:
    rate(200)
    for p in ps:
        p.pos = p.pos + p.p * dt



