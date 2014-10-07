from __future__ import division
from visual import *
from visual.graph import *
from math import *
from sys import argv

### Parameters
N  = int(argv[1])
dx = 2/(N-1)
R  = dx / 8
e  = 1.602e-19


### Scene
scene = display( title = 'Coulomb potential', x=0, y=0, width=600, height=600, center = (0,0,0))
scene.range = 3.
scene.autoscale = False
scene.forward   = ( 0, 0, -1 )

graph = gdisplay(title = 'Coulomb potential', x=600, y=0, width=600, height=600, ymax = 1e-18 )

### Particles
particles = {}
for i in range(N):
    x = -1 + i * dx
    y = 0
    z = 0
    particles[i] = sphere( pos = (x,y,z), radius = R, mass = e, color = color.blue )


### Functions
def Distance( particle, point = vector(0.,0.,0.) ):
    epsilon = 1e-6
    if isinstance( point, sphere ):
        point = point.pos
    return (particle.pos-point).mag if (particle.pos-point).mag > epsilon else epsilon

def IncreaseCharge( index ):
    particles[index].mass += e

def DecreaseCharge( index ):
    particles[index].mass -= e

def CreateParticle( position, charge = e ):
    global N
    N += 1
    particles[N] = sphere( pos = position, radius = R, mass = charge, color = color.orange )


def ChangeStatus( click, left = True ):
    index = None
    for i in particles:
        if abs(click.pos[0] - particles[i].x) < 2*R:
            index = i
            break

    if index is None:
        CreateParticle( (click.pos[0],y,z) )
    elif left:
        IncreaseCharge( index )
    else:
        DecreaseCharge( index )
    PlotPotential()

def Potential( here ):
    if not isinstance( here, vector ):
        here = vector(here,0,0)
    const  = 1 / (4*pi)
    return const * sum([particles[i].mass/Distance(particles[i],here) for i in particles])

def SamplePotential( N = 1000 ):
    x = [ -2 + i/250 for i in range(N) ]
    V = map( Potential, x )
    return x,V

def PlotPotential():
    global points
    try:
        points.dot = ()
    except:
        pass
    points = gcurve( color = color.red )
    points.plot( pos = zip(*SamplePotential()), accumulate = False )

scene.bind('click',ChangeStatus)
PlotPotential()
help(points)
while True:
    rate(200)
