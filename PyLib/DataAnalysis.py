#
# Module with some functions for data analysis.
# Note: Be careful with covariance algorithm
#
# Author: Gonzalo Martinez
#
# Last update: 17 / 03 / 2014
#

from math import *

def Mean( data, weights=None ):
    ''' Returns the average value for a given list of numbers. It can be either a list/tuple or a dictionary with the weight asociated to each value.'''
    
    if not weights:
        if isinstance( data, dict ):
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
    
    if isinstance( data, list ):
        if len( data ) % 2:
            return sorted( data ) [ len( data ) / 2 ]
        
        return 0.5 * ( sorted( data ) [ len( data ) / 2 - 1 ] + sorted( data ) [ len( data ) / 2 ] )
    
    data2 = map( lambda x: x[1], sorted( data.items() ) )
    acum = Cumulative( data2 )
    tot = acum[-1]
    
    if tot/2 in acum:
        return d[ acum.index( tot/2 ) ]
    
    f1 = filter( lambda x: x > tot/2 , acum )[0]
    index = acum.index( f1 )
    f0 = acum[ index - 1 ]
    a1 = data[ index ]
    a0 = data[ index - 1 ]
    
    return a0 + ( .5 * tot - f0 ) / ( f1 - f0 ) * ( a1 - a0 )

def Mode( data ):
    ''' Returns the mode of a sample. The argument must be a list/tuple with data or a dictionary with pairs value - frecuency.'''
    
    if isinstance( data, (list,tuple) ):
        return Mode( Frecs( data ) )
    
    return sorted( Izip( data.items() ) )[-1][1]

def Covariance( x, y, weights = None, xmean = None, ymean = None ):
    ''' Returns the covariance between two lists of data.'''

    if len(x) == len(y) < 2:
        return None
    
    if not xmean or not ymean:
        xmean = Mean( x, weights )
        ymean = Mean( y, weights )
    
    if not weights:
        return sum( map( lambda x,y: ( x - xmean ) * ( y - ymean ), x, y ) ) / float( len(x) )
    
    normfactor = sum( weights )**2 - sum ( map( lambda x: x**2, weights ) )
    normfactor = sum( weights )/normfactor
    
    return normfactor * sum( map( lambda x,y,w: w * ( x - xmean ) * ( y - ymean ), x, y, weights ) )

def Correlation( x, y, weigths = None, xmean = None, ymean = None ):
    ''' Returns the correlation factor between two lists of data.'''
    
    return Covariance( x, y, weights, xmean, ymean ) / ( RMS( x, weights, xmean ) * RMS( y, weights, ymean ) )

def Chi2( exp, sexp, th ):
    ''' Calculates the Chi2 for a given set of data exp compared with its expected value th and uncertaintities sexp.'''
    
    if not len(exp) == len(sexp) == len(th):
        raise ValueError('The arguments must have the same size.')

    return sum( map( lambda x,y,z: ( ( x - y ) / z )**2, exp, th, sexp ) )









