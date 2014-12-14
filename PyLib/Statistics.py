'''
    Module with some important functions about statistics and the distribution class.
    Some important destributions are already coded.
    
    @Author: G. Martinez lema
    @Date  : 22 / 10 / 2014
'''

from __future__ import division
import operator
import math
import Math
import General
import Sequences
import Plots
import random
import Array

def Mean( data, weights = None ):
    '''
        Returns the average for a given set of data. It can be either a sequence or a dictionary with the weight asociated to each value.
    '''
    
    if isinstance( data, dict ):
        return Mean( *zip( *data.items() ) )
    elif weights:
        return reduce( operator.add, map( operator.mul, data, weights ) ) / sum( weights )
    else:
        return reduce( operator.add, data ) / len( data )

def Covariance( x, y, weights = None, xmean = None, ymean = None ):
    '''
        Returns the covariance between two sequences of data.
    '''
    
    if len(x) == len(y) < 2:
        return 0.
    
    xmean = Mean( x, weights ) if xmean is None else xmean
    ymean = Mean( y, weights ) if ymean is None else ymean

    if weights:
        V1 = sum( weights )
        V2 = sum ( wi**2 for wi in weights )
        normfactor = V1/ ( V1**2 - V2 )
        return normfactor * sum( map( lambda x,y,w: w * ( x - xmean ) * ( y - ymean ), x, y, weights ) )
    else:
        return sum( map( lambda x,y: ( x - xmean ) * ( y - ymean ), x, y ) ) / ( len(x) - 1. )

def Variance( data, weights = None, datamean = None ):
    '''
        Returns the variance for a given list of numbers. It can be either a list/tuple or a dictionary with the weight asociated to each value. It also accepts the mean of the distribution as a parameter.
    '''
    return Covariance( data, data, weights, datamean, datamean )

def RMS( data, weights = None, datamean = None ):
    '''
        Returns the standard desviation for a given list of numbers. It can be either a list/tuple or a dictionary with the uncertainty asociated to each value. It also accepts the mean of the distribution as a parameter.
    '''
    return math.sqrt( Variance( data, weights, datamean ) )

def Correlation( x, y, weights = None, xmean = None, ymean = None ):
    '''
        Returns the correlation factor between two lists of data.
    '''
    return Covariance( x, y, weights, xmean, ymean ) / ( RMS( x, weights, xmean ) * RMS( y, weights, ymean ) )

def CovarianceMatrix( *args, **kwargs ):
    '''
        Compute the covariance matrix of the input dataset. Weights must be set as keyword argument: weights = None (default).
    '''
    
    weights = kwargs.get('weights')
    N   = len( args )
    CVM = Array.Zeros( N, N )
    means = [ Mean(x,weights) for x in args ]
    for i in range(N):
        x = args[i]
        for j in range(i,N):
            CVM[i][j] = Covariance( x, args[j], weights, means[i], means[j] )
            if i == j: # Just to dont sum twice when summing the transpose
                CVM[i][j] *= .5

    return CVM + CVM.T()

def CorrelationMatrix( *args, **kwargs ):
    '''
        Compute the correlation matrix of the input dataset. Weights must be set as keyword argument: weights = None (default).
    '''
    
    weights = kwargs.get('weights')
    N   = len( args )
    CRM = Array.Identity( N ) * 0.5
    means = [ Mean(x,weights) for x in args ]
    for i in range(N):
        x = args[i]
        for j in range(i+1,N):
            CRM[i][j] = Correlation( x, args[j], weights, means[i], means[j] )
    
    return CRM + CRM.T()

def Skewness( data, weights = None, datamean = None, datavariance = None ):
    '''
        Compute skewness for a dataset with or without weights. NOT CHECKED
    '''
    if datamean is None:
        datamean     = Mean(data,weights)
    if datavariance is None:
        datavariance = Variance( data, weights, datamean )
    
    if weights:
        V1 = sum( weights )
        V2 = sum ( wi**2 for wi in weights )
        V3 = sum ( wi**3 for wi in weights )
        normfactor = V1**2/ ( V1**3 - 3 * V1 * V2 + 2 * V3 )
        return normfactor * sum( wi * ( xi - datamean ) ** 3 for xi,wi in zip( data, weights ) )
    else:
        ndata = len(data)
        return sum( ( xi - datamean )**3 for xi in data ) * ndata / ( ( ndata - 1. ) * ( ndata - 2. ) )

def Kurtosis( data, weights = None, datamean = None, datavariance = None, dataskewness = None ):
    '''
        Compute kurtosis for a dataset with or without weights. NOT CHECKED
    '''
    
    if datamean is None:
        datamean     = Mean(data,weights)
    if datavariance is None:
        datavariance = Variance( data, weights, datamean )
    if dataskewness is None:
        dataskewness = Skewness( data, weights, datamean, datavariance )

    if weights:
        V1 = sum( weights )
        V2 = sum ( wi**2 for wi in weights )
        V3 = sum ( wi**3 for wi in weights )
        V4 = sum ( wi**4 for wi in weights )
        normfactor4 = V1 * ( V1**4 - 4 * V1 * V3 + 3 * V2**2 ) / ( ( V1**2 - V2 ) * ( V1**4 - 6 * V1**2 * V2 + 8 * V1 * V3 + 3 * V2**2 - 6 * V4 ) )
        normfactor2 = 3 * ( V1**2 - V2 ) * ( V1**4 - 2 * V1**2 * V2 + 4 * V1 * V3 - 3 * V2**2 ) / ( V1**2 * ( V1**4 - 6 * V1**2 * V2 + 8 * V1 * V3 + 3 * V2**2 - 6 * V4 ) )
        return normfactor4 * sum( wi * ( xi - datamean ) ** 4 for xi,wi in zip( data, weights ) ) - normfactor2 * datavariance
    else:
        ndata = len(data)
        return sum( ( xi - datamean )**4 for xi in data ) * ndata * ( ndata + 1. ) / ( ( ndata - 1. ) * ( ndata - 2. ) * ( ndata - 3. ) ) - 3 * ( ndata - 1. )**2 / ( ( ndata - 2. ) * ( ndata - 3. ) ) * datavariance**2

def Weights( uncertainties ):
    '''
        Returns the associated weigths for a set of uncertainties.
    '''
    
    return map( lambda x: math.pow( x, -2. ), uncertainties )

def Median( data ):
    '''
        Returns the median of a sample. The argument must be a sequence or a dictionary of values and frecuencies.
    '''
    
    if isinstance( data, list ):
        return sorted( data ) [ len( data ) / 2 ] if len( data ) % 2 else Mean( sorted( data ) [ len( data ) / 2 - 1 : len( data ) / 2 + 1] )
    elif isinstance( data, dict ):
        x, y = zip( *sorted( data.items() ) )
        cum  = Sequences.Cumulative( y )
        tot  = cum[-1]
        half = tot/2
        if half in cum:
            return x[ cum.index( half ) ]
        else:
            for i in xrange(len(cum)):
                if cum[i] > half:
                    break

            f1 = cum[ i     ]
            f0 = cum[ i - 1 ]
            a1 = x  [ i     ]
            a0 = x  [ i - 1 ]
            return a0 + ( half - f0 ) / ( f1 - f0 ) * ( a1 - a0 )

def Mode( data ):
    '''
        Returns the mode of a sample. The argument must be a list/tuple with data or a dictionary with pairs value - frecuency.
    '''
    if isinstance( data, dict ):
        return max( *Sequences.Izip( sorted(data.items()) ) )[1]
    else:
        return Mode( Sequences.Frequencies( data ) )

def Chi2( exp, sexp, th ):
    '''
        Calculates the Chi2 for a given set of data exp compared with its expected value th and uncertaintities sexp.
    '''
    return sum( map( lambda x,y,z: ( ( x - y ) / z )**2, exp, th, sexp ) )

class Distribution:
    '''
        Class for distributions.
    '''
    
    def __init__( self, pdf = None, lower = 0., upper = 1., Npoints = 100000, integer = False, normalized = True ):
        '''
            Constructor. Use a pdf in a range lower-upper with Npoints. It the distribution is not normalized set normalized to False.
            To construct this class with a set of data check the FromData method.
        '''
        self.integer  = integer
        self.lower    = lower
        self.upper    = upper
        self.Npoints  = upper - lower if self.integer else General.rint(Npoints)
        self.delta    = (upper-lower)//Npoints if self.integer else (upper-lower)/Npoints
        self.pdf      = pdf
        if not normalized:
            self._Normalize()
        
        self.xvalues  = self._GetBins( self.Npoints, self.lower, self.upper )
        self.yvalues  = map( self.pdf, self.xvalues )
        self.dict     = dict( zip( self.xvalues, self.yvalues ) )
        
        self._ComputeCDF()
        self._ComputeICDF()
        
        self.mean     = Mean( self.xvalues, self.yvalues )
        self.variance = Variance( self.xvalues, self.yvalues, self.mean )
        self.rms      = math.sqrt( self.variance )
        self.median   = Median( self.dict )
        self.mode     = Mode( self.dict )

        self.random   = random.Random()
            
    def _Normalize( self ):
        inverseintegral = math.pow( self.Integral(), -1 )
        f = self.pdf
        self.pdf = lambda x: inverseintegral * f(x)

    def _GetBins( self, N, lower, upper ):
        if self.integer:
            return range(lower,upper,(upper-lower)//N)
        N = General.rint(N)
        delta = 0.5 * float( upper - lower ) / N
        return Sequences.Binning( N, lower + delta, upper + delta )

    def _ComputeCDF( self ):
        '''
            Compute the cumulative density function of the probability density function from lower with step = delta. Upper is the upper limit from which cdf = 1.
        '''
        def cumulative( x ):
            return 0. if x <= self.lower else 1. if x >= self.upper else self.Integral( upper = x )
        self.cdf = cumulative

    def _ComputeICDF( self ):
        '''
            Compute the cumulative density function of the probability density function from lower with step = delta. Upper is the upper limit from which cdf = 1.
        '''
        if self.integer:
            def icumulative(x):
                sum = 0
                x0 = self.lower - 1
                while sum<x:
                    x0  += 1
                    sum += self.pdf(x0)

                return x0
        else:
            def icumulative( x, p = self.delta ):
                low = self.lower
                up  = self.upper
                dif = p + 1
            
                while abs(dif) > p:
                    x0 = ( up + low ) / 2
                    dif = self.cdf( x0 ) - x
                    if dif > 0:
                        up = x0
                    else:
                        low = x0
                return x0
        
        self.icdf = icumulative

    def Integral( self, lower = None, upper = None, Npoints = None ):
        '''
            Compute integral from lower to upper with Npoints.
        '''
        lower   = self.lower if lower is None else lower
        upper   = self.upper if upper is None else upper
        Npoints = self.Npoints if Npoints is None else Npoints

        return sum(range(lower,upper+1)) if self.integer else sum( map( self.pdf, self._GetBins( Npoints, lower, upper ) ) ) * float( upper - lower ) / Npoints

    def IsNormalized( self, tolerance = 1e-3 ):
        '''
            Check normalization with a given tolerance.
        '''
        return 1 - tolerance < self.Integral() < 1 + tolerance

    def PDFHistogram( self ):
        '''
            Make an histogram of the PDF.
        '''
        return Plots.MakeH1( sorted(self.dict.items()) )

    def CDFHistogram( self ):
        '''
            Make an histogram with the distribution data.
        '''
        yvalues = map( self.cdf, self.xvalues )
        return Plots.MakeH1( sorted( zip( self.xvalues, yvalues )  ) )

    @staticmethod
    def FromData( xvals, yvals, OutOfRange = False ):
        '''
            Construct this class from a x,y-dataset. This is performed by interpolating linearly the data.
        '''
        return Distribution( Math.Interpolate( xvals, yvals, OutOfRange ), xvals[0], xvals[-1], normalized = False )

    def __call__( self, x, fun = 'pdf' ):
        '''
            Call fun.
        '''
        exec( 'fun =  self.' + fun )
        return fun(x)

    def Random( self, p = None ):
        '''
            Return a random value with the distribution of the pdf.
        '''
        p = self.delta if p is None else p
        return self.icdf( self.random.uniform(0,1), p )

def Poisson( mean, upper = None ):
    '''
        Poisson distribution with mean mean: ( mean**k / k! ) exp(-mean)
    '''
    assert mean <=25, 'Mean value too large. For large mean value (lambda) the Poisson distribution can be approximated by a gaussian with mean = variance = lambda'
    if upper is None:
        upper = 4 * mean
    upper = General.cint( upper )
    norm = math.exp( -mean )
    return Distribution( lambda k: norm * math.pow(mean,k) / Math.Factorial(k), 0, upper, upper, integer = True )

def Binomial( p, N ):
    '''
        Binomial distribution: N! / ( k! (N-k)! ) p**k ( 1 - p )**k
    '''
    assert 0 < p < 1,'p must be a probability: 0 < p < 1'
    q = 1. - p
    return Distribution( lambda k: Math.BinomialCoefficient(N,k) * math.pow( p, k ) * math.pow( q, N - k ), 0, N, N, integer = True )

def Gauss( mean = 0., sigma = 1., lower = None, upper = None, Npoints = 1e4 ):
    '''
        Gaussian distribution with mean mean and standard deviation sigma: 1 / ( sqrt( 2 pi ) sigma  ) * exp( -( x - x0 ) / ( 2 sigma**2 ) )
    '''
    if lower is None:
        lower = mean - 5 * sigma
    if upper is None:
        upper = mean + 5 * sigma

    norm = 1. / ( math.sqrt( 2 * math.pi ) * sigma )
    expo = .5 / sigma**2

    return Distribution( lambda x: norm * math.exp( - expo * (x-mean)**2 ), lower, upper, Npoints )

def Gamma( k, theta, upper = None, Npoints = 1e4 ):
    '''
        Gamma distribution with shape k and scale theta: 1/( Gamma(k) theta**k) x**(k-1) exp(-x/theta).
        Where Gamma is the Euler Gamma.
    '''
    if upper is None:
        upper = 10 * math.pow( k, .5 + 1e-3 * k ) * theta
    
    norm = math.pow( Math.Gamma(k) * math.pow(theta,k), -1 )
    return Distribution( lambda x: norm * math.pow( x, k-1 ) * math.exp( - x / theta ), 0, upper, Npoints )

def Exponential( theta, upper = None, Npoints = 1e4 ):
    '''
        Exponential distribution with scale factor theta: 1/theta exp(-x/theta).
    '''

    if upper is None:
        upper = -theta * math.log(1e-3)
        
    norm = math.pow( theta, -1 )
    return Distribution( lambda x: norm * math.exp( - x / theta ), 0, upper, Npoints )

def ChiSquared( ndof, upper = None, Npoints = 1e4 ):
    '''
        Chi squared distribution.
    '''
    if ndof > 200:
        raise ValueError('Number of degrees of freedom too large. For ndof>200, the distribution can be approximated by a gaussian with mean ndof and sigma sqrt(2*ndof)')
    
    if upper is None:
        upper = 10. + 2 * ndof

    if ndof % 2:
        norm = math.sqrt( 2 * math.pi ) * Math.DoubleFactorial( ndof - 2 )
    else:
        norm = math.pow( 2, ndof/2 ) * Math.Factorial( ndof/2 - 1 )
    
    norm = math.pow( norm, -1 )
    expo = 0.5 * ndof - 1.
    
    return Distribution( lambda x: norm * math.pow( x, expo) * math.exp( - 0.5 * x ), 0, upper, Npoints )

def tStudent( ndof, lower = -10, upper = 10, Npoints = 1e4 ):
    '''
        t-Student distribution.
    '''
    if ndof > 200:
        raise ValueError('Number of degrees of freedom too large. For ndof>200, the distribution can be approximated by a normal gaussian.')
    
    if ndof % 2:
        norm = Math.Factorial( ( ndof-1 )/2 ) * math.pow( 2, ( ndof-1 ) / 2 ) / ( math.pi * math.sqrt( ndof ) * Math.DoubleFactorial( ndof-2 ) )
    else:
        norm = Math.DoubleFactorial( ndof - 1 ) / ( math.pow( 2, ndof/2 ) * math.sqrt( ndof ) * Math.Factorial(  ndof/2 - 1 ) )
    
    indof = math.pow( ndof, -1 )
    expo  = - ( 1. + ndof ) / 2
    
    return Distribution( lambda x: norm * math.pow( 1. + indof * x ** 2, expo ), lower, upper, Npoints )

if __name__ == '__main__':
    mean = 5.
    sigma = 2.
    g = Gauss( mean, sigma, Npoints = 5e3 )
    print 'gaussian distribution with mean {0} and sigma {1}'.format(mean,sigma)
    print 'integral = ', g.Integral()
    print 'cumulative at mean = ', g.cdf(mean)
    print 'inverse cumulative at 0.5 = ', g.icdf(.5)
    print 'mean: ', g.mean
    print 'rms:  ', g.rms
    print 'median: ', g.median
    print 'mode: ', g.mode
    print '\n'
    
    mean = 5
    p = Poisson( mean )
    print 'poissonian distribution with mean {0}'.format(mean)
    print 'integral = ', p.Integral()
    print 'cumulative at mean = ', p.cdf(mean)
    print 'inverse cumulative at 0.5 = ', p.icdf(.5)
    print 'mean: ', p.mean
    print 'rms:  ', p.rms
    print 'median: ', p.median
    print 'mode: ', p.mode
