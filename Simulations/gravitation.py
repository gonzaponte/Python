from visual import *
from visual.graph import *
from ROOT import TRandom3
from math import *
from General import *

def dr(p1,p2):
    return p1.pos - p2.pos

def r(p1,p2):
    return mag(dr(p1,p2))

def force(cte,p1,p2):
    return -cte*dr(p1,p2)/r(p1,p2)**3

R  = TRandom3()
R.SetSeed(0)
U  = R.Uniform
V  = lambda A: A * ( 2. * U() - 1. )
UA = 149597870700. # m
km = 1e3 # m
kg = 1   # kg

G   = 6.67384e-11
dt = 3600*6.*100

M0   = 10**8 * kg
R0   = 10**9 * km
V0   = 10**1 * km
Rmax = 10**10 * km

print 'creating particles...'

def create( n ):
    global particles
    
    if n==1:
        particles = [ sphere( pos    = ( V(Rmax), 0., 0. ),
                      radius = R0,
                      color  = color.red,
                      p      = M0 * V0 * vector( V(1), 0., 0. ),
                      make_trail = False ) for i in range(100) ]

    elif n==2:
        particles = [ sphere( pos    = ( V(Rmax), V(Rmax), 0. ),
                             radius = R0,
                             color  = color.red,
                             p      = M0 * V0 * vector( V(1), V(1), 0. ),
                             make_trail = False ) for i in range(100) ]

    elif n==3:
        particles = [ sphere( pos    = ( V(Rmax), V(Rmax), V(Rmax) ),
                      radius = R0,
                      color  = color.red,
                      p      = M0 * V0 * vector( V(1), V(1), V(1) ),
                      make_trail = False ) for i in range(100) ]

create(2)
rlp = range(len(particles))

print 'GO!'
while True:
    rate(200)
    F = [ vector(0.,0.,0.) for i in rlp ]
    for i in rlp:
        pi = particles[i]
        for j in rlp[i+1:]:
            pj    = particles[j]
            fij   = force( G * M0**2, pi, pj ) #reduce( SUM, map( lambda pj: force( G * M0**2, pi, pj ), particles[i+1:] ) )
            F[i] += fij
            F[j] -= fij

    for i in rlp:
        particles[i].p   = particles[i].p   - F[i] * dt
        particles[i].pos = particles[i].pos + particles[i].p/M0 * dt








