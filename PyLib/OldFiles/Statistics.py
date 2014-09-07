#
# Module with some important statistical functions.
#
#
# Author: Gonzalo Martinez
#
# Note: Be careful with covariance algorithm
#

from check import *
from math import *

def Mean( data, weights=None ):
    ''' Returns the average value for a given list of numbers. It can be either a list/tuple or a dictionary with the weight asociated to each value.'''
    
    if not iscontainer( data ):
        wrong( Mean )
    
    if not weights:
        if isdic( data ):
            return Mean( data.keys(), data.values() )
        
        return sum( data ) / float( len( data ) )
    
    return sum( map( lambda x,y: x * y, data, weights ) ) / sum( weights )

def Variance( data, weights = None, datamean = None ):
    ''' Returns the variance for a given list of numbers. It can be either a list/tuple or a dictionary with the weight asociated to each value. It also accepts the mean of the distribution as a parameter.'''
    
    return Covariance( data, data, weights, datamean, datamean )

def RMS( data, weights = None, datamean = None ):
    ''' Returns the standard desviation for a given list of numbers. It can be either a list/tuple or a dictionary with the uncertainty asociated to each value. It also accepts the mean of the distribution as a parameter.'''
    
    return sqrt( Variance( data, weights ) )

def Weights( uncertainties ):
    ''' Returns the associated weigths to a set of uncertainties.'''
    
    return map( lambda x: x ** -2., uncertainties )

def Median( data ):
    ''' Returns the median of a sample. The argument must be a list/tuple or data or a dictionary of values and frecuencies.'''
    
    if islist( data ):
        if len( data ) % 2:
            return sorted( data ) [ len( data ) / 2 ]
        
        return 0.5 * ( sorted( data ) [ len( data ) / 2 - 1 ] + sorted( data ) [ len( data ) / 2 ] )
    
    data = sorted( data.items() )
    acum = Acumulate( data )
    tot  = sum( zip( *data ) [1] )
    
    if tot/2 in acum:
        return d[ acum.index( tot/2 ) ]
    
    f1 = filter( lambda x: x > tot/2 , acum )[0]
    index = acum.index( f1 )
    f0 = acum[ index - 1 ]
    a1 = d[ index ]
    a0 = d[ index - 1 ]
    
    return a0 + ( .5 * tot - f0 ) / ( f1 - f0 ) * ( a1 - a0 )

def Mode( data ):
    ''' Returns the mode of a sample. The argument must be a list/tuple with data or a dictionary with pairs value - frecuency.'''
    
    if islist( data ) or istuple( data ):
        return Mode( Frecs( data ) )
    
    return sorted( Izip( data.items() ) )[-1][1]

def Covariance( x, y, weigths = None, xmean = None, ymean = None ):
    ''' Returns the covariance between two lists of data.'''
    
    if not iscontainer(x) or not iscontainer(y) or not HaveSameLength(x,y):
        wrong(Covariance)
    
    if not xmean or not ymean:
        xmean = Mean( x, weights )
        ymean = Mean( y, weights )

    if not weights:
        return sum( map( lambda x,y: ( x - xmean ) * ( y - ymean ), x, y ) ) / sfloat( len(x) )

    #    normfactor = sum( weights )**2 - sum ( map( lambda x: x**2, weights ) )
    #    normfactor = sum( weights )/normfactor
    normfactor = 1. / sum( weights )
    
    return normfactor * sum( map( lambda x,y,w: w * ( x - xmean ) * ( y - ymean ), x, y, weights ) )



def Correlation( x, y, weigths = None, xmean = None, ymean = None ):
    ''' Returns the correlation factor between two lists of data.'''
    
    return Covariance( x, y, weights, xmean, ymean ) / ( RMS( x, weights, xmean ) * RMS( y, weights, ymean ) )



class Distribution:
    def __init__( self, pdf = None, lower = 0., upper = 1., delta = 1e-6):
        self.pdf         = pdf
        self.cdf         = None
        self.mean        = None
        self.variance    = None
        self.RMS         = None
        self.bins        = None
        self.pdfsample   = None
        self.cdfsample   = None

        self.low      = float( lower )
        self.upper    = float( upper )
        self.delta    = delta

        self.Compute_sample()
        self.Compute_cdf()
        self.Compute_mean()
        self.Compute_variance()
        self.Compute_RMS()

    def Compute_sample( self ):
        self.bins      = binning( ( self.upper - self.lower ) / self.delta, self.lower, self.upper )
        self.pdfsample = map( self.pdf, self.bins )
    
    def Compute_cdf( self ):
        self.cdf       = lambda xn: sum( map( self.pdf, self.bins[: int( ( xn - self.lower )/self.delta ) ] ) ) * self.delta
        self.cdfsample = map( self.cdf, self.bins )

    def Compute_mean( self ):
        self.mean = Mean( self.bins, self.pdfsample )

    def Compute_variance( self ):
        self.variance = Variance( self.bins, self.pdfsample, self.mean )

    def Compute_RMS( self ):
        self.RMS = sqrt( self.variance )










