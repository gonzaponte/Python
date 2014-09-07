from visual import *
from visual.graph import *
from ROOT import TRandom3
from math import *
from scipy import array
from Constants import c
from scipy.optimize import *

R  = TRandom3()
R.SetSeed(0)
U  = R.Uniform
V  = lambda A: A * ( 2. * U() - 1. )
P  = R.Poisson

MeV = 1e6
GeV = 1e9
TeV = 1e12

um = us = 1e-6
nm = ns = 1e-9
pm = ps = 1e-12
fm = fs = 1e-15

d0 = .5 * nm
r0 = 0.81 * fm
Nm = 26

s  = 7 * TeV
dt = 1e-6 * fs

mp = 937.232 * MeV
Ep = s/2
pp = sqrt( Ep**2 - mp**2 )
gp = Ep/mp
bp = sqrt( 1 - gp**-2 )
vp = bp * c
print vp*dt


def SumVector( vs ):
    return reduce( lambda x,y: x+y, vs )

def GetVector( p, theta ):
    return p * vector( cos(theta), sin(theta), 0. )

def GetVectors( ps, ts ):
    return [ GetVector(p,t) for p,t in zip(ps,ts) ]

def Ptotal( ts, ps ):
    return SumVector( GetVectors(ps,ts) ).mag

scene = display( title = 'LHCb collision', x=0, y=0, width=1200, height=675, center=(0,0,0.) )

p1 = sphere( pos   = ( -d0, 0., 0. ),
            radius = r0,
            color  = color.red,
            p      = +vp * vector( 1., 0., 0. ),
            make_trail = True )

p2 = sphere( pos    = ( +d0, 0., 0. ),
            radius = r0,
            color  = color.red,
            p      = -vp * vector( 1., 0., 0. ),
            make_trail = True )

while (p2.pos - p1.pos).mag > 1 * pm:
    rate(200)
    p1.pos = p1.pos + p1.p * dt
    p2.pos = p2.pos + p2.p * dt

p1.visible = False
p2.visible = False
del p1
del p2

N = P( Nm )

Es = [ U()     for i in range(N) ]; Es = [ E * s / sum(Es) for E in Es]
ms = [ U() * E for E in Es       ]
ps = [ sqrt( E**2 - m**2 ) for E,m in zip(Es,ms) ]
gs = [ E/m for E,m in zip(Es,ms) ]
bs = [ sqrt( 1 - g**-2 ) for g in gs ]
vs = [ b * c for b in bs ]
print 'antes'
ts = tuple( fmin( Ptotal, array( [0.] * N ), (ps,), 1e-6, 1e10, 1e10 ) )
print ts, Ptotal( ts, ps )

raise ValueError()

Ps = [sphere( pos   = ( 0., 0., 0. ),
             radius = m/s,
             color  = color.green,
             p      = d,
             make_trail = True ) for m,d in zip(ms,ds) ]

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



