from __future__ import division
from Math import Factorial, DoubleFactorial
from math import *
from Plots import Plot4D

def linspace( x0, x1, N = 100 ):
    dx = (x1-x0)/N
    return [ x0 + i*dx for i in range(N) ]

def Legendre( l, m ):
    if m>l:
        raise ValueError( "m must not be greater than l" )
    if not l:
        return lambda x: 1

    if m < 0:
        return lambda x: (-1)**m * Factorial(l+m)/Factorial(l-m) * Legendre(l,-m)(x)

    if l == m:
        return lambda x: (-1)**l * DoubleFactorial( 2*l-1 ) * ( 1 - x**2 ) ** (l/2)

    if m == l - 1:
        return lambda x: ( 2*m+1 ) * x * Legendre( m, m )(x)

    return lambda x: 1/(l-m) * ( ( 2*l - 1 ) * x * Legendre(l-1,m)(x) - (l-1+m)*Legendre(l-2,m)(x) )


def SphericalHarmonic( l, m ):
    return lambda ctheta, phi: (-1)**m * ( (2*l+1) / (4*pi) * Factorial(l-m)/Factorial(l+m) )**(1/2) * Legendre( l, m )( ctheta ) * cos( phi )

N = 100
r = 1
ctheta = linspace( -1, 1 )
ctheta = [ ct for ct in ctheta for j in range(N) ]
theta  = map( acos, ctheta )
phi    = linspace(  0, 2*pi, N ) * len(theta)
x      = [ sin(t) * cos(p) for t,p in zip(theta,phi) ]
y      = [ sin(t) * sin(p) for t,p in zip(theta,phi) ]
z      = list(ctheta)

l = m = 0
SH = SphericalHarmonic( l, m )
E = map( SH, ctheta, phi )

a = Plot4D( x, y, z, E )

