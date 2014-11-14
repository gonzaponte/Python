#
# Module that contains useful mathematical functions
# Note: include 2D/3D numerical integration and LU methods for solving and for matrix inversion.
#
# Author: Gonzalo Martinez
#
# Last update: 01 / 11 / 2014
#
from __future__ import division

import math
import random

import Sequences
import Array

def Factorial( N ):
    '''
        Factorial function.
    '''
    assert isinstance( N, int ), ValueError( 'The factorial function is only defined for integers. Use Gamma for real numbers.' )
    assert N >=   0,    ValueError( 'The factorial function is only defined for positive numbers.' )
    assert N <= 170, OverflowError( 'Input too large.' )
    return N * Factorial( N - 1 ) if N else 1

def DoubleFactorial( N ):
    '''
        Double factorial function.
    '''
    assert isinstance( N, int ), ValueError( 'The double factorial function is only defined for integers.' )
    assert N >=   0,    ValueError( 'The double factorial function only defined for positive numbers.' )
    assert N <= 300, OverflowError( 'Input too large.' )
    return N * DoubleFactorial( N - 2 ) if N > 1 else 1

def Asymmetry( x, y ):
    '''
        Asymmetry factor, i.e. (x-y)/(x+y).
    '''
    return ( x - y ) / ( x + y )

def Sign( x ):
    '''
        Sign function. -1 for negative numbers, 1 otherwise.
    '''
    return -1 if x < 0 else 1

def LogGamma( x ):
    '''
        log( Gamma(x) ) where Gamma is the Euler-Gamma function.
    '''
    assert x >= 0, ValueError( 'Euler Gamma is only defined for positive numbers.' )
    t  =   x + 5.5
    t -= ( x + 0.5 ) * math.log( t )
    y  =  1.000000000190015
    y += 76.18009172947146     / ( x + 1. )
    y -= 86.50532032941677     / ( x + 2. )
    y += 24.01409824083091     / ( x + 3. )
    y -=  1.231739572450155    / ( x + 4. )
    y +=  0.001208650973866179 / ( x + 5. )
    y -=  0.5395239384953e-5   / ( x + 6. )
    
    return math.log( 2.5066282746310005 * y / x ) - t

def Gamma( x ):
    '''
        Euler Gamma function: integral_0^inf{ t^(x-1) exp(-t) dt }
    '''
    assert x >= 0, ValueError( 'Euler Gamma is only defined for positive numbers.' )
    return math.exp( LogGamma( x ) )

def Beta( x, y ):
    '''
        Beta function.
    '''
    assert x >= 0 and y>=0, ValueError( 'Euler Gamma is only defined for positive numbers.' )
    return math.exp( logGamma( x ) + logGamma( y ) - logGamma( x + y ) )

def Erf( x, p = 1e-20 ):
    '''
        Error function up to x with precision p.
    '''
    if not x:
        return 0.
    
    dif = p + 1.
    new = 0.
    n   = 0
    
    while dif > p:
        old  = new
        new += x ** ( 2 * n + 1 ) / ( ( 2*n + 1. ) * Factorial( n ) )
        n   += 1
        new -= x ** ( 2 * n + 1 ) / ( ( 2*n + 1. ) * Factorial( n ) )
        n   += 1
        dif  = abs( 1. - old/new )
    
    return 2. * new / math.sqrt( math.pi )

def Cerf( x, p = 1e-20 ):
    '''
        Complementary error function from x with precision p.
    '''
    return 1. - Erf( x, p )

def Bessel( n, p = 1e-20 ):
    '''
        1st kind nth-Bessel function with precision p.
    '''
    
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
    '''
        Calculates the root of a transcedental equation of type x = f(x) with precision p and an initial estimation x0.
    '''
    
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
    ''' 
        Solves a differential equation using the Runge-Kutta method. The equation must be of the form: y' = F(x,y) with the initial values x0,y0.
        The solution is a vector from x0 to x1 with the number of steps given by the precision dx.
    '''
    
    y = list()
    N = int( math.ceil( (x1-x0)/dx ) )
    
    for i in xrange(N):
        k1  = F( x0           , y0               )
        k2  = F( x0 + 0.5*dx  , y0 +   0.5*dx*k1 )
        k3  = F( x0 + 0.5*dx  , y0 +   0.5*dx*k2 )
        k4  = F( x0 +     dx  , y0 +       dx*k3 )
        y  += [ y0 + ( k1 +2*k2 + 2*k3 + k4 )*dx/6. ]
        x0 += dx
        y0  = y[-1]
    
    return y

def PolynomialInterpolator( xdata, ydata ):
    '''
        Returns a polynomial interpolator of degree npoints - 1 for xdata, ydata.
    '''
    A = Array.Matrix( map( lambda x: [ x**i for i in range(len(xdata)) ], xdata ) )
    B = Array.Vector( *ydata )
    return Polynom( A.Inverse() ** B )

def LinearInterpolator( xdata, ydata, OutOfRange = False ):
    '''
        Returns a linear interpolator for xdata, ydata. Set OutOfRange to True to coerce out of range inputs to the limits. It raises an error otherwise.
    '''
    n = len(xdata)
    def interpolator(x0):
        found = False
        for i in range(n-1):
            if x0 >= xdata[i] and x0 < xdata[i+1]:
                x1, x2 = xdata[i:i+2]
                y1, y2 = ydata[i:i+2]
                found = True
                break
        if not found:
            if OutOfRange:
                return ydata[0] if x0 < xdata[0] else ydata[-1]
            else:
                raise ValueError('x0 = {0} out of range'.format(x0) )
        
        slope = (y2-y1)/(x2-x1)
        const = y1 - slope * x1
        
        return slope * x0 + const

def SplineInterpolator( xdata, ydata, order = 3 ):
    '''
        Returns a spline interpolator for xdata, ydata of a given order < npoints. order must be an odd number to perform better.
    '''
    ndata = len(xdata)
    nleft = (order+1)//2 - 1
    nright = nleft + 2
    def interpolator(x0):
        found = False
        for i in range(ndata-1):
            if x0 >= xdata[i] and x0 < xdata[i+1]:
                found = True
                if i < nleft:
                    xsubset = xdata[:order+1]
                    ysubset = ydata[:order+1]
                elif i == ndata + 1 - nright:
                    xsubset = xdata[-order-1:]
                    ysubset = ydata[-order-1:]
                else:
                    xsubset = xdata[i-nleft:i+nright]
                    ysubset = ydata[i-nleft:i+nright]
                break
        if not found:
            raise RuntimeError( 'Data point {0} out of range [{1},{2})'.format(x0,xdata[0],xdata[-1]) )
        return PolynomialInterpolator( xsubset, ysubset )(x0)
    return interpolator

def FindRoots( F, lower, upper, ndivs = 1e5 ):
    '''
        Finds the roots of a function.
    '''
    
    ndivs = int( round(ndivs) )
    div = ( lower - upper ) / (ndivs)
    f0 = F(lower)
    
    roots = []
    for i in xrange( ndivs ):
        f = F( lower + i * div )
        if ( Sign(f) != Sign(f0) ):
            roots += [ lower + ( i - 0.5 ) * div ]
        
        f0 = f

    return roots

def Root( F, lower, upper, precision = 1e-6, timeout = 1e9 ):
    '''
        Find the root of the function F in the interval [lower,upper].
    '''
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
    
    print 'Root not found. Try to increase the timeout.'
    return None

def Integral( F, lower, upper, p = 1e-3 ):
    '''
        Performs numerical integration of the function F from lower to upper with precision p.
    '''
    
    d = float( upper - lower )
    
    error = 1 + p
    f, f2, N = 0, 0, 0
    R = random.Random()
    
    while 0 != error > p:
        N    += 1
        x     = min + d * R.Uniform(0,1)
        fx    = F( x )
        f    += fx
        f2   += fx**2
        error = d * math.sqrt( abs( f2 / N**2 - f**2 / N**3 ) )
    
    return d * f / N, error

def Solve2( p2, p1, p0 ):
    '''
        Solves a 2nd degree polynomial.
    '''
    
    a = ( p1**2 - 4 * p2 * p0 )**.5
    return -.5 * ( p1 - a ) / p2, -.5 * ( p1 + a ) / p2

def Derivative( F, x, N = 1, h = 1e-4 ):
    '''
        Returns the derivative of order N the function F at x with step size h.
    '''

    a = Solve( [ [ (j - 2.)**i for j in range(5) ] + [ Factorial(N) if i == N else 0. ] for i in range(5) ] )
    
    return sum( [ a[i] * f( x + (i-2) * h ) for i in range(5) ] ) / h**n

def Solve( M, N = None ):
    '''
        Solves a system of equations. The input must be in matrix form; it accepts both a matrix of coeficients with the independent terms joined or separated. The return is a vector of values.
    '''

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
    
    return [ ( m[i][-1] - sum( [ x[j] * m[i][j] for j in range( i+1, f ) ] ) ) / m[i][i] for i in Sequences.Reversed(range(f)) ]

class Polynom:
    '''
        Good performance of polynoms.
    '''

    def __init__( self, coefs ):
        '''
            Polinom with the given coefficients in power-increasing order: a0 + a1 x + a2 x2 + ... + an xn
        '''
        self.coefs   = tuple(coefs)
        self.n       = len(self.coefs)
        self.degree  = self.n - 1
    
    def _subpol( self ):
        '''
            Create subpolinom: a1 + a2 x + a3 x2 + ... 
        '''
        return self.__class__( self.coefs[1:] ) if self.degree else self.__class__([])

    def Derivative( self, k = 1 ):
        '''
            Compute kth-derivative.
        '''
        der = self.__class__(self.coefs)
        for i in range(k):
            der = der._Derivative()
        return der
        
    def _Derivative( self ):
        '''
            Compute first derivative.
        '''
        return self.__class__( [ i * self.coefs[i] for i in range(1,self.n) ] )

    def __call__( self, x ):
        '''
            Evaluate.
        '''
        return self.coefs[0] + x * self._subpol()(x) if self.n else 0.

    def __str__( self ):
        return ' + '.join( [ '{0} x{1}'.format(coef,i) for i,coef in enumerate(self.coefs) ] )


class Fitter:
    '''
        Class for data fitting.
    '''
    def __init__( self, xdata, ydata ):
        assert len(xdata) == len(ydata), 'Datasets must have the same length'
        self.x = list( xdata )
        self.y = list( ydata )
        self.N = len(xdata)

#   Need a multidimensional optimizer
#    def Fit( self, fun, args0 ):
#        '''
#            Fit to a general function fun.
#        '''
#        chi2 = sum( lambda x,y: (x-y)**2, self.ydata, map( fun(args),self.xdata) )
#        Optimizer =


    def PolyFit( self, degree = 1 ):
        '''
            Performs the fit solving A x = B where x are the coeficients of the pol.
        '''
        a = [ [1.] * self.N ] + [ map( lambda x: math.pow( x, n+1 ), self.x) for n in range(degree) ]
        a = Array.Matrix(*a)
        b = Array.Vector(*self.y)
        
        self.A = a ** a.T()
        self.B = a ** b
        self.AI = self.A.Inverse()
        self.coefs = list(self.AI ** self.B)
        f = lambda x: sum( [self.coefs[i]*math.pow(x,i) for i in range(degree+1)] )
        chi2 = sum( [ math.pow( y - f(x), 2 ) for x,y in zip(self.x,self.y) ] )
        syx = math.sqrt( chi2 / ( self.N - degree - 1 ) )
        
        self.coefs_errors = [ syx * math.sqrt( self.AI[i][i] ) for i in range(degree+1) ]
        return zip( self.coefs, self.coefs_errors )

class Optimizer:
    '''
        Class for extrema finding.
    '''
    def __init__( self, F, xmin, xmax ):
        '''
            Initilize with some function F in a interval [xmin,xmax].
        '''
        self.ndim = len(xmin) if isinstance( xmin, (list,tuple) ) else 1
        self.fun  = F
        self.xmin = tuple(xmin) if isinstance( xmin, (list,tuple) ) else xmin
        self.xmax = tuple(xmax) if isinstance( xmax, (list,tuple) ) else xmax
        self.gold = ( 3 - math.sqrt(5) ) / 2 #golden ratio to perform better
    
    def Minimize( self, x0 = None, max_size = 1e-6, xmin = None, xmax = None ):
        return self._Minimize1D( x0, max_size, xmin, xmax ) if self.ndim is 1 else self._MinimizeND( x0, max_size, xmin, xmax )

    def Maximize( self, x0 = None, max_size = 1e-6, xmin = None, xmax = None ):
        return self._Maximize1D( x0, max_size, xmin, xmax ) if self.ndim is 1 else self._MaximizeND( x0, max_size, xmin, xmax )

    def _Minimize1D( self, x0 = None, max_size = 1e-6, xmin = None, xmax = None ):
        '''
            Brackets a minimum in the interval [xmin,xmax] in a smaller interval of size <= max_size.
            Output: ( minimum, minimum - lower limit, upper limit - minimum), f(minimum)
            Default values for xmin and xmax are those of the constructor.
        '''
        a = self.xmin if xmin is None else xmin
        c = self.xmax if xmax is None else xmax
        b = self._FirstMiddlePoint( a, c ) if x0 is None else x0
        
        while (c-a) > max_size:
            fb  = self.fun( b )
            new, closetoa = self._MiddlePoint( a, b, c )
            fnew = self.fun( new )
            if fnew < fb:
                a, b, c = (a, new, b) if closetoa else (b, new, c)
            else:
                a, b, c = (new, b, c) if closetoa else (a, b, new)
                
        return (new,new-a,b-new), fnew

    def _MinimizeND( self, x0 = None, v0 = None, max_size = 1e-6, xmin = (), xmax = (), max_iter = 1e5 ):
        v0 = Array.Identity(self.ndim) if v0 is None else v0
        
        x  = Array.Vector(x0)
        v  = Array.Matrix(v0)
        
        x0 = Array.Vector(x0)
        fx = self.fun( x0 )
        
        niterations = -1
        while True:
            niterations += 1
            
            fx1    = fx
            bigdim = 0
            bigval = 0.
            for i in range(self.ndim):
                fx2 = fx
                x, v1, fx =  self._MinimizeAlongPath( x, v[i] )
                if fx2 - fx > bigval:
                    bigval = fx2 - fx
                    bigdim = i
        
            if 2 * ( fx1 - fx ) <= max_size * ( abs(fx1) + abs(fx) + 1e-6 ):
                return
            
            if niterations > max_iter:
                return None
            
            x1 = 2 * x0 - x
            v1 = x0 - x
            x  = x0
            
            fx1 = 0

    def _MinimizeAlongPath( self, P, V ):
        F1D = lambda x: self.fun( *(P + x * V) )
        xmin,fxmin = Optimizer( F1D, 0., 1. ).Minimize()
        Vnew = xmin[0] * V
        Pnew = P + Vnew
        return Pnew, Vnew, fxmin
    

    def _Maximize1D( self, x0 = None, max_size = 1e-6, xmin = None, xmax = None ):
        '''
            Brackets a maximum in the interval [xmin,xmax] in a smaller interval of size <= max_size.
            Output: ( maximum, maximum - lower limit, upper limit - maximum), f(maximum)
            Default values for xmin and xmax are those of the constructor.
        '''
        original = self.fun
        self.fun = lambda *args: -original(*args)
        output = self.Minimize( x0, max_size, xmin, xmax )
        self.fun = original
        return output[0], -output[1]

    def _FirstMiddlePoint( self, a, c ):
        '''
            Gets a random point within the interval where the function takes a smaller value than the limits to start iteration.
        '''
        R = random.Random()
        limit = min( self.fun(a), self.fun(c) )
        while True:
            point = random.uniform( a, c )
            if self.fun(point) < limit:
                return point

    def _MiddlePoint( self, a, b, c ):
        '''
            Return the middle point for the next iteration.
        '''
        return ( b - self.gold * ( b - a ), True ) if b - a > c - b else ( b + self.gold * ( c - b ), False )

class Interpolator:
    '''
        A class to interpolate data with splines of arbitrary odd-order (order < npoints).
    '''
    def __init__( self, xdata, ydata, order = 3 ):
        self.xdata = list(xdata)
        self.ydata = list(ydata)
        self.ndata = len(xdata)
        self.order = order
        self.left  = (order+1)//2 - 1
        self.right = self.left + 2

    def __call__( self, x0 ):
        '''
            Get interpolated value at x0.
        '''
        found = False
        for i in xrange(self.ndata-1):
            if x0 >= self.xdata[i] and x0 < self.xdata[i+1]:
                found = True
                if i < self.left:
                    xsubset = self.xdata[:self.order+1]
                    ysubset = self.ydata[:self.order+1]
                elif i == self.ndata + 1 - self.right:
                    xsubset = self.xdata[-self.order-1:]
                    ysubset = self.ydata[-self.order-1:]
                else:
                    xsubset = self.xdata[i-self.left:i+self.right]
                    ysubset = self.ydata[i-self.left:i+self.right]
                break
        if not found:
            raise RuntimeError( 'Data point {0} out of range [{1},{2})'.format(x0,self.xdata[0],self.xdata[-1]) )
        return PolynomialInterpolator( xsubset, ysubset )(x0)


if __name__ == '__main__':
    from math import sin,log
    from ROOT import *
    fun = lambda x: log(x) - sin(x)**2
    x = map(float, range(1,101))
    y = map( fun, x )

    interpolator = Interpolator( x, y, 7 )

    xfull = [ 0.1*i for i in range(10,1000)]
    yfull = map( interpolator, xfull )
    yreal = map( fun, xfull )
    
    data = TGraph(); data.SetMarkerStyle(20)
    curve = TGraph();curve.SetLineColor(2);curve.SetLineWidth(2)
    real = TGraph();real.SetLineColor(4);real.SetLineWidth(2)
    [data.SetPoint(i,xi,yi) for i,(xi,yi) in enumerate(zip(x,y))]
    [curve.SetPoint(i,xi,yi) for i,(xi,yi) in enumerate(zip(xfull,yfull))]
    [real.SetPoint(i,xi,yi) for i,(xi,yi) in enumerate(zip(xfull,yreal))]
    real.Draw('AC')
    curve.Draw('sameC')
    data.Draw('sameP')

