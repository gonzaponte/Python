#
# Module that contains useful mathematical functions
# Note: include 2D/3D numerical integration and LU methods for solving and for matrix inversion.
#
# Author: Gonzalo Martinez
#
# Last update: 08 / 04 / 2014
#

from math import *
from Sequences import Reversed, Zeros, Identity
from ROOT import TRandom3 # use other module for randoms if ROOT is not available

def Factorial( N ):
    ''' Returns x factorial.'''
    return N * Factorial( N - 1 ) if N else 1

def DoubleFactorial( N ):
    ''' Returns x double factorial.'''
    
    return N * DoubleFactorial( N - 2 ) if N > 1 else 1

def Asymmetry( x, y ):
    ''' This function returns the asymmetry factor between two values.'''
    
    return ( x - y ) / float( x + y )

def Sign( x ):
    ''' Sign function.'''
    
    return -1 if x < 0 else 1

def LogGamma( x ):
    ''' Returns the value log( Gamma(x) ). The argument must be a positive real number. '''
    
    t  = x + 5.5
    t -= ( x + 0.5 ) * log( t )
    y  =  1.000000000190015
    y += 76.18009172947146     / ( x + 1. )
    y -= 86.50532032941677     / ( x + 2. )
    y += 24.01409824083091     / ( x + 3. )
    y -=  1.231739572450155    / ( x + 4. )
    y +=  0.001208650973866179 / ( x + 5. )
    y -=  0.5395239384953e-5   / ( x + 6. )
    
    return log( 2.5066282746310005 * y / x ) - t

def Gamma( x ):
    ''' Returns the value of evaluating the Gamma function at x.'''
    
    return exp( LogGamma( x ) )

def Beta( x, y ):
    ''' Returns the value of evaluating the Beta function at x,y.'''
    
    return exp( logGamma( x ) + logGamma( y ) - logGamma( x + y ) )

def Erf( x, p = 1e-20 ):
    ''' Returns the value of the error function up to x with precision p.'''
    
    if not x:
        return 0.
    
    dif = p + 1.
    new = 0.
    n = 0
    while dif > p:
        old = new
        new += x ** ( 2 * n + 1 ) / ( ( 2*n + 1. ) * Factorial( n ) )
        n   += 1
        new -= x ** ( 2 * n + 1 ) / ( ( 2*n + 1. ) * Factorial( n ) )
        n   += 1
        dif  = abs( 1. - old/new )
    
    return 2. * new / sqrt( pi )

def Cerf( x, p = 1e-20 ):
    ''' Returns the value of the complementary error function from x with precision p.'''
    
    return 1. - Erf( x, p )

def Bessel( n, p = 1e-20 ):
    ''' Returns the value of the 1st kind nth-Bessel function with precision p.'''
    
    besselsign = -1 if n < 0 and n % 2 else 1
    
    def bessel( x ):
        dif = p + 1
        m   = 0
        new = 0.
        x  *= 0.5
        
        while dif > p:
            old = new
            new += x ** ( 2*m + n ) / ( Factorial( m ) * Factorial( m + n ) )
            m += 1
            new -= x ** ( 2*m + n ) / ( Factorial( m ) * Factorial( m + n ) )
            m += 1
            dif = abs( 1. - old/new )
        
        return besselsign * new
    
    return bessel

def Recursive( f, x0 = 0., p = 1e-12 ):
    ''' Calculates the root of a transcedental equation of type x = f(x). x0 is an approach to the root and p the precision.'''
    
    new = 0.
    dif = p + 1
    N   = 0
    
    while dif > p:
        N  += 1
        y   = f( x0 )
        dif = abs( 1. - x0/y )
        x0  = y
        
        if N > 1000000:
            print 'The solution does not converge'
            return None
    
    return x0

def RK4( F, x0, y0, x1, dx = 1e-6 ):
    ''' Solves a differential ecuation by the Runge-Kutta method. The ecuation must be of the form: y' = F(x,y) with the initial values x0,y0. The solution is a vector from x0 to x1 with the number of steps given by the precision dx.'''
    
    y = list()
    N = int( ceil( (x1-x0)/dx ) )
    
    for i in xrange(N):
        k1  = F( x0           , y0               )
        k2  = F( x0 + 0.5*dx  , y0 +   0.5*dx*k1 )
        k3  = F( x0 + 0.5*dx  , y0 +   0.5*dx*k2 )
        k4  = F( x0 +     dx  , y0 +       dx*k3 )
        y  += [ y0 + ( k1 +2*k2 + 2*k3 + k4 )*dx/6. ]
        x0 += dx
        y0  = y[-1]
    
    return y

#def Interpolate( xs, ys, opt = 'float' ):
#    ''' This function takes two lists and returs the function that passes by all points obtained by linear interpolation.'''
#    
#    xs, ys = zip( *sorted( zip( xs, ys ) ) )
#    
#    def Interpolator( x0 ):
#        for i in xrange( 1, len(xs) ):
#            if xs[i] >= x0:
#                x1, y1 = xs[ i - 1 ], ys[ i - 1 ]
#                x2, y2 = xs[   i   ], ys[   i   ]
#                break
#    
#        m = float( y2 - y1 ) / ( x2 - x1 ) if not x1 == x2 else 0.
#        n = y1 - m * x1
#        
#        return m * x0 + n if opt == 'float' else int( m * x0 + n )
#    
#    return Interpolator

def Interpolate( xvals, yvals, OutOfRange = False ):
    '''
        Construct this class from a x,y-dataset. This is performed by interpolating linearly the data.
    '''
    
    n = len(xvals)
    def interpolator(x0):
        found = False
        for i in range(n-1):
            if x0 > xvals[i] and x0 < xvals[i+1]:
                x1, x2 = xvals[i:i+2]
                y1, y2 = yvals[i:i+2]
                found = True
                break
        if not found:
            if OutOfRange:
                return yvals[0] if x0 < xvals[0] else yvals[-1]
            else:
                raise ValueError('x0 = {0} out of range'.format(x0) )
        
        slope = float(y2-y1)/(x2-x1)
        const = y1 - slope * x1
        
        return slope * x0 + const


def FindRoots( F, lower, upper, ndivs = 1e5 ):
    ''' Finds the roots of a function.'''
    
    ndivs = rint(ndivs)
    div = ( lower - upper ) / float(ndivs)
    f0 = F(lower)
    
    roots = []
    for i in xrange( ndivs ):
        f = F( lower + i * div )
        if ( Sign(f) != Sign(f0) ):
            roots += [ lower + ( i - 0.5 ) * div ]
        
        f0 = f

    return roots

def Root( F, lower, upper, precision = 1e-6, timeout = 1e9 ):
    ''' Find the root of the function F in the interval lower-upper.'''
    lower, upper = float(lower), float(upper)
    flower, fupper = F(lower), F(upper)
    
    counter = 0
    while counter < timeout:
        middle  = lower - flower * ( upper - lower ) / ( fupper - flower )
        fmiddle = F(middle)
        
        if abs( fmiddle ) < precision:
            return middle
        
        elif Sign( fmiddle ) == Sign( flower ):
            lower  =  middle
            flower = fmiddle
        
        elif Sign( fmiddle ) == Sign( fupper ):
            upper  =  middle
            fupper = fmiddle

        counter += 1
    
    print 'Root not found. If youre sure that it must be there, increase the timeout.'
    return None

def Integral( F, lower, upper, p = 1e-3 ):
    ''' Performs numerical integration of the function F from lower to upper with precision p.'''
    
    d = float( upper - lower )
    
    error = 1 + p
    f, f2, N = 0, 0, 0
    
    while 0 != error > p:
        N    += 1
        x     = min + d * R.Rndm()
        fx    = F( x )
        f    += fx
        f2   += fx**2
        error = d * sqrt( abs( f2 / N**2 - f**2 / N**3 ) )
    
    return d * f / N, error

def Solve2( p2, p1, p0 ):
    ''' Solves a 2nd degree polynomial.'''
    
    a   = p1**2 - 4 * p2 * p0
    a **= .5
    
    return -.5 * ( p1 - a ) / p2, -.5 * ( p1 + a ) / p2

def Derivative( F, x, N = 1, h = 1e-4 ):
    ''' Returns the derivative of order N the function F at x with step size h.'''

    a = Solve( [ [ (j - 2.)**i for j in range(5) ] + [ Factorial(N) if i == N else 0. ] for i in range(5) ] )
    
    return sum( [ a[i] * f( x + (i-2) * h ) for i in range(5) ] ) / h**n

def Det( M ):
    ''' Returns the determinan of a matrix.'''
    
    l = len(M)
    if l == 1:
        return M[0][0]
    
    elif l == 2:
        return Det2(M)
    
    elif l == 3:
        return Det3(M)
    
    else:
        raise ValueError('The matrix is too big, maximum size = 3')


def Det2( M ):
    ''' Returns the determinant of a 2 by 2 matrix.'''
    
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]

def Det3( M ):
    ''' Returns the determinant of a 3 by 3 matrix.'''
    
    det  = 0
    det += m[0][0] * m[1][1] * m[2][2]
    det += m[0][1] * m[1][2] * m[2][0]
    det += m[0][2] * m[1][0] * m[2][1]
    det -= m[0][2] * m[1][1] * m[2][0]
    det -= m[0][1] * m[1][0] * m[2][2]
    det -= m[0][0] * m[1][2] * m[2][1]
    
    return det


def Solve( M, N = None ):
    ''' Solves a system of equations. The input must be in matrix form; it accepts both a matrix of coeficients with the independent terms joined or separated. The return is a vector of values.'''

    f = len( m )
    c = f + 1
    
    def Pivoting( m, x ):
        ''' Pivotes on the matrix m to put the biggest element in column x in (x,x).'''
        
        maxval = abs( m[x][x] )
        maxpos = x

        for i in range( x+1, f ):
            if abs( m[i][x] ) > maxval:
                maxval = abs(m[i][x])
                maxpos = i

        for i in range(c):
            aux          = m[x][i]
            m[x][i]      = m[maxpos][i]
            m[maxpos][i] = aux

        return m

    if N:
        for i in range(f):
            m[i].append(n[i])
    
    for i in range(f):
        M = Pivoting( M, i )
        for j in range( i+1, f ):
            factor = m[j][i] / m[i][i]
            m[j] = map( lambda x,y: x - factor * y, m[j], m[i] )
    
    return [ ( m[i][-1] - sum( [ x[j] * m[i][j] for j in range( i+1, f ) ] ) ) / m[i][i] for i in Reversed(range(f)) ]

def MxM( M1, M2 ):
    ''' This function performs a matrix product between M1 and M2.'''
    
    rows1 = len( M1 )
    cols1 = len( M1[0] )
    cols2 = len( M2[0] )
    
    M = Zeros( rows1, cols2 )
    
    for i in range(rows1):
        for j in range(cols2):
            for k in range(cols1):
                M[i][j]+= M1[i][k] * M2[k][j]
    
    return M

def Transpose( M ):
    ''' Performs matrix transpose.'''
    
    return [ [M[j][i] for j in range(len(M))] for i in range(len(M[0])) ]

def Diagonalize( M0, p=1e-4 ):
    ''' Performs the diagonalization of a simetric matrix using the Jacobi algorithm. The parameter p defines what is 0 for your calculus.'''
    
    def findmax( M ):
        maximum = 0.
        maxpos  = [ 0, 0 ]
        for i in range( len( M ) ):
            for j in range( len( M[0] ) ):
                if i==j:
                    continue
                if abs( M[i][j] ) > maximum:
                    maximum = abs( M[i][j] )
                    maxpos  = [i,j]
        return maxpos
    
    def check( M ):
        for i in range( len(M) ):
            for j in range( i+1, len( M[0] ) ):
                if abs( M[i][j] ) > p :
                    return False
        return True
    
    D  = list( M0 )
    V  = Identity( len(M0) )
    
    while not check(D):
        row, col = findmax( D )
        
        t = ( D[col][col] - D[row][row] ) / ( 2. * D[row][col] )
        t = Sign(t) / ( abs(t) + sqrt( t**2 + 1 ) )
        c = 1. / sqrt( t**2 + 1 )
        s = c * t
        
        R = Identity( len(M) )
        R[row][row] =  c
        R[col][col] =  c
        R[row][col] =  s
        R[col][row] = -s
        
        D = MxM( Transpose( R ), MxM( D, R ) )
        V = MxM( V, R )
    
    return D, V



