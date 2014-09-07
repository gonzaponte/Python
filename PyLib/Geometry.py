#
# Module with some geometrical operations.
#
#
# Author: Gonzalo Martinez
#
# Last update: 15 / 08 / 2014
#

from math import *

def module( v ):
    return sqrt( sum( [vi**2 for vi in v] ) )

def scale( v, f ):
    return tuple([ vi * f for vi in v ])

def scalardot( v, w ):
    return sum( [ vi * wi for vi,wi in zip(v,w) ] )

def DOCA( p, q, v ):
    d = ( p[0] - q[0], p[1] - q[1], p[2] - q[2] )
    dmod = module(d)
    vmod = module(v)
    d = scale( d, 1./dmod )
    v = scale( v, 1./vmod )
    phi = acos( scalardot( d, v ) )
    theta = 0.5 * pi - phi
    return dmod * cos( theta )

