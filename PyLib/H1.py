#
# Module with the histogram class.
# Note: not updated, not checked.
#
# Author: Gonzalo Martinez
#
# Last update: --/--/--
#

from Sequences import Zeros, Binning
try:
    from ROOT import TH1,TH1F
    _is_root_present = True
except:
    print 'The ROOT module is not present. ROOT-related functions will not be available.'
    _is_root_present = False

class H1:
    ''' 1D histogram.'''
    
    def __init__( self, nbins = 100, low = 0., up = 1., title = 'h1', xtitle = '', ytitle = 'Entries' ):
        ''' Class constructor. It takes the number of bins, the lower and upper limits and the titles of the histogram. Default values:
            nbins = 100
            low   = 0
            up    = 1
            title = 'h1' 
            xtitle = #nothing#
            ytitle = Entries
        '''
                
        self.nbins  = int( nbins )
        self.low    = float( low )
        self.up     = float(  up )
        self.delta  = ( self.up - self.low ) / self.nbins
        self.halfdelta = 0.5 * self.delta
        
        self.title  = title
        self.xtitle = xtitle
        self.ytitle = ytitle
        
        # Includes underflow and overflow bins
        self.xbins      = Binning( self.nbins, self.low + self.halfdelta, self.up + self.halfdelta )
        self.xunderflow = 0
        self.xoverflow  = 0
        self.xentries   = map( int, Zeros( nbins ) )
    
        self.ncalls   = 0
        self.integral = 0

    def __repr__(self):
        '''
            Printing.
        '''
        return '\n\n'.join([ ' '.join( map( str, [self.xunderflow] + self.xentries + [self.xoverflow] ) ), ' '.join( map( str, ['u'] + self.xbins + ['o'] ) ) ])

    def FindBin( self, value ):
        '''
            Find bin for input value.
        '''
        return -1 if value < self.low else int( ( value - self.low ) // self.delta ) if value < self.up else self.nbins

    def Fill( self, value ):
        '''
            Fill values.
        '''
        self.ncalls   += 1
        self.integral += 1
        
        bin = self.FindBin( value )
        if 0 <= bin < self.nbins:
            self.xentries[bin] += 1
        elif bin < 0:
            self.xunderflow += 1
        else:
            self.xoverflow += 1
        return bin
    
    def SetBinContent( self, bin, value ):
        '''
            Set bin content to value.
        '''
        self.ncalls   += 1
        self.integral += value
        
        if 0 <= bin < self.nbins:
            self.xentries[bin] += 1
        elif bin < 0:
            self.xunderflow += 1
        else:
            self.xoverflow += 1
        return bin
    
    def Import( self, H ):
        '''
            Import histogram from ROOT's TH1.
        '''
        assert _is_root_present, 'ROOT module not present. Function unavailable.'
        assert isinstance(H,TH1), 'Input histogram is not an instance of TH1.'
        
        self = H1( H.GetNbinsX(), H.GetXaxis().GetXmin(), H.GetXaxis().GetXmax(), H.GetTitle(), H.GetXaxis().GetTitle(), H.GetYaxis().GetTitle() )
        bins = range( nbins + 2 )
        
        self.ncalls = H.GetEntries()
        self.integral = H.Integral()
        return map( self.SetBinContent, bins, map( H.GetBinContent, bins ) )

    def Export( self, name = None, instance = TH1F ):
        '''
            Export histogram to ROOT's TH1 format.
        '''
        assert _is_root_present, 'ROOT module not present. Function unavailable.'
        
        name = self.title if name is None else name
        title = ';'.join( [ self.title, self.xtitle, self.ytitle ] )
        th1 = instance(name,title, self.nbins, self.low, self.up )
        
        th1.SetBinContent(0,self.xunderflow)
        for bin in range(self.nbins):
            th1.SetBinContent(bin+1,self.xentries[bin])
        th1.SetBinContent(self.nbins+1,self.xoverflow)
        
        return th1
        
    
    def GetBinContent( self, bin ):
        '''
            Get the content of the bin.
        '''
        return self.xunderflow if bin < 0 else self.xentries[bin] if bin < self.nbins else self.xoverflow
    
    def Integral( self, x0 = -float('inf'), x1 = float('inf') ):
        '''
            Return integral.
        '''
        bin0 = max( 0, self.FindBin( x0 ) )
        bin1 = min( self.nbins, self.FindBin( x1 ) + 1 )
        
        return sum( self.xentries[bin0:bin1] ) * self.delta
    
    def __add__( self, other ):
        '''
            Sum histograms.
        '''
        assert self.xbins == other.xbins, 'Histograms cannot be summed: different binning.'
        
        map( Fill(self.Bin(i)[0], other.Bin(i)[1] ) )
        return self
    
    def Copy(self):
        
        histo = H1(self.nbins, self.low, self.up, self.title, self.xtitle, self.ytitle )
        histo.xunderflow = self.xunderflow
        histo.xoverflow  = self.xoverflow
        histo.xentries   = list(self.xentries)
        histo.ncalls     = self.ncalls
        histo.integral   = self.integral
        return histo
    
    def GetMean( self ):
        '''
            Mean of the histogram.
        '''
        return Mean( self.xbins, self.xentries )
    
    def GetMedian( self ):
        '''
            Median of the histogram.
        '''
        sum  = 0.
        for bin,entry in enumerate(self.xentries):
            sum += entry
            if sum/self.integral > 0.5:
                return self.xbins[bin]
        return float('inf')
    
    def GetMode( self ):
        '''
            Mode of the histogram.
        '''
        bin = self.xentries.index( max(self.xentries) )
        return self.xbins[bin]


from RandomNumbers import *

R = LCG()

h = H1(100,0,100,'x')
bins = map( h.Fill, [R.Gauss(50,20) for i in range(10000)] )
print bins
print h

th = h.Export()
th.Draw()
