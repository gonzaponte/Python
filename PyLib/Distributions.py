#
# Module with some important distributions.
# Note: May need a non-data based distribution class: just with functions (saves memory)
#
# Author: Gonzalo Martinez
#
# Last update: 17 / 03 / 2014
#

from math import *
from Math import factorial, doublefactorial, Interpolate
from Sequences import Binning, Cumulative, Scale
from DataAnalysis import *
from Plots import MakeH1, GoodLooking, GetMax

def Poisson( l ):
    ''' Returns the Poisson pdf with mean l.'''
    
    norm = exp( -l )
    
    return lambda k: norm * l**k / factorial(k)

def Gauss( x0 = 0., sigma = 1.):
    ''' Returns a gaussian pdf with mean x0 and half width sigma.'''
    
    norm = 1. / ( sqrt( 2*pi ) * sigma )
    expo = 1. / sigma**2
    
    return lambda x: norm * exp( - 0.5 * expo * (x-x0)**2 )

def ChiSquared( k ):
    ''' Returns the Chi2 pdf with k degrees of freedom.'''

    if k % 2:
        norm = sqrt( 2 * pi ) * doublefactorial( k - 2 )
    else:
        norm = 2**(k/2) * factorial( k/2 - 1 )
    
    norm = 1. / norm
    expo = 0.5 * k - 1.
    
    return lambda x: norm * x ** expo * exp( - 0.5 * x )

def tStudent( v ):
    ''' Returns the pdf of a t-Student distribution.'''
    
    if v % 2:
        norm = factorial( ( v - 1 )/2 ) * 2 ** ( ( v - 1 ) / 2 ) / ( pi * sqrt( v ) * doublefactorial( v - 2 ) )
    else:
        norm = doublefactorial( v - 1 ) / ( 2 ** ( v/2 ) * sqrt( v ) * factorial(  v/2 - 1 ) )
    
    iv   = 1. / v
    expo = - 0.5 * ( 1. + v )
    
    return lambda x: norm * ( 1. + iv * x ** 2 ) ** expo

class Distribution:
    ''' This class contains all the tools and structures needed for statistical analysis.'''
    
    def __init__( self, pdf = None, lower = 0., upper = 1., delta = 1e-5):
        ''' Class constructor. It can be constructed with a function that represents the pdf. It can also be constructed empty if you want to construct the class from some data set. In this case you shall use the "CreatePDF" method.'''
        
        self.GENERATOR = pdf
        self.BINS      = Binning( ( upper - lower ) / delta, lower, upper )
        self.low       = float( lower )
        self.up        = float( upper )
        self.delta     = float( delta )
        self.Npoints   = len( self.BINS )
        self.points    = xrange( self.Npoints )
        
        self.PDF       = None
        self.CDF       = None
        self.MEAN      = None
        self.RMS       = None
        self.VARIANCE  = None
    
        self.__Compute_pdf()
    
    def cdf( self ):
        ''' Returns the cdf of the distribution and stores it in the data members. '''
        
        if not self.CDF:
            self.__Compute_cdf()
        
        return self.CDF
    
    def pdf( self ):
        ''' Returns the pdf of the distribution.'''
        
        return self.PDF
    
    def cdfAt( self, x ):
        ''' Returns the value of the cdf at x.'''
        if not self.CDF:
            self.__Compute_cdf()
        
        return self.CDF[ self.GetIndex( x ) ]
    
    def pdfAt( self, x ):
        ''' Returns the value of the cdf at x.'''
        
        return self.PDF[ self.GetIndex( x ) ]
    
    def GetIndex( self, x ):
        ''' Returns the closest index below x.'''
        
        for i in self.points:
            if self.BINS[ i ] > x:
                return i - 1
        
        return -1
    
    def mean( self ):
        ''' Returns the mean of the distribution.'''
        
        if self.MEAN is None:
            self.__Compute_mean()
        
        return self.MEAN
    
    def rms( self ):
        ''' Returns the rms of the distribution.'''
        
        if self.RMS is None:
            self.__Compute_RMS()
        
        return self.RMS

    def variance( self ):
        ''' Returns the variance of the distribution.'''
        
        if self.VARIANCE is None:
            self.__Compute_variance()
        
        return self.VARIANCE
    
    def Print( self, name = 'mydistribution', cdf = False ):
        ''' Creates a plot of the distribution.'''
        
        from ROOT import TCanvas, gStyle
        c = TCanvas()
        gStyle.SetOptStat('')
        
        self.pdfhisto = MakeH1( zip( self.BINS, self.PDF ), name, self.Npoints )
        GoodLooking( self.pdfhisto, 1 )
        self.pdfhisto.Draw()
    
        if cdf:
            if not self.CDF:
                self.__Compute_cdf()
            
            self.cdfhisto = MakeH1( zip(self.BINS,self.CDF), name + 'cdf', self.Npoints )
            GoodLooking( self.cdfhisto, 2 )
            self.cdfhisto.Scale( GetMax( self.pdfhisto ) )
            self.cdfhisto.Draw('same')
        
        c.Update()
        return c
    
    def CreatePDF( self, xs, ys ):
        self.__init__( Interpolate( xs, ys ), self.low, self.up, self.delta )
    
    def __Compute_mean( self ):
        ''' Computes the mean.'''
        
        self.MEAN = Mean( self.BINS, self.PDF )

    def __Compute_variance( self ):
        ''' Computes the variance.'''
        
        if self.MEAN is None:
            self.__Compute_mean()
        self.VARIANCE = Variance( self.BINS, self.PDF, self.MEAN )

    def __Compute_RMS( self ):
        ''' Computes the RMS.'''
        
        if self.VARIANCE is None:
            self.__Compute_variance()
        self.RMS = sqrt( self.VARIANCE )

    def __Compute_pdf( self ):
        ''' Computes the pdfsample in order to save computation time.'''
        
        self.PDF = map( self.GENERATOR, self.BINS )
    
    def __Compute_cdf( self ):
        self.CDF = Scale( Cumulative( self.PDF ), self.delta )
#        self.cdf       = lambda xn: sum( map( self.pdf, self.bins[: int( ( xn - self.lower )/self.delta ) ] ) ) * self.delta
#        self.cdfsample = map( self.cdf, self.bins )

