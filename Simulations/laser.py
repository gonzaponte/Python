from visual import *
from visual.graph import *
from math import *
from random import random
r = random

setattr( sphere, 'inside', True )

dt      = 5e-02                # temporal step
L0      = 10.                  # laser length
R0      = 1.                   # laser radius
Zmax    = 20.                  # maximum distance for photons
r0      = 0.1                  # photons radius
P       = 1e-2                 # probability of creating new photons
T       = 1e-2                 # Probability of transfer photons
x0      = ( 0., 0., 1.001*r0 ) # initial positions for photons
p0      = vector( 0., 0., 1. ) # initial momentum for photons
violet  = ( 0.4, 0.0, 1.0 )    # violet color
photons = []                   # list of photons


# Scene
scene = display( title = 'Laser simulation', x=0, y=0, width=1200, height=675, center=(0,0,L0/2.) )
scene.autoscale = False
scene.forward   = ( 1, 0, 0 )

# Laser
tube   = cylinder( pos = x0, radius = R0, axis = ( 0., 0., L0 ), color = color.green, opacity = 0.2 )

# Initial photon
photons += [ sphere( pos = x0, radius = r0, p = p0, color = violet ) ]

# Advance in time
while True:
    rate(200)
    
    # Create new photons
    for i in range( len( photons ) ):
        photon = photons[i]
        if photon.inside and r()<P:
            print 'new photon'
            photons += [ sphere( pos = tuple(photon.pos), radius = r0, p = vector(photon.p), color = violet ) ]
            photons[-1].pos -= photons[-1].p*dt

    # Propagate photons
    for i in range( len(photons) ):
        photon = photons[i]
        if photon.inside:
            if photon.z <= r0:
                photon.p *= -1
            if photon.z >= ( L0 - r0 ):
                if r()<T:
                    photon.inside = False
                else:
                    photon.p *= -1
        photon.pos = photon.pos + photon.p * dt

    # Delete leaving photons
    for i in range( len( photons ) )[::-1]:
        if not photons[i].inside and photons[i].z >= Zmax:
            photons[i].visible = False
            del photons[i]


