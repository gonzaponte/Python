#
# Module with the histogram class.
# Note: not updated, not checked.
#
# Author: Gonzalo Martinez
#
# Last update: --/--/--
#

from Sequences import Zeros, Binning
from Dictionaries import StrDic

class H1:
    ''' 1D histogram.'''
    
    def __init__( self, nbins = 100, low = 0., up = 1., title = 'h1' ):
        ''' Class constructor. It takes the number of bins, the lower and upper limits and the title of the histogram. Axis labels might be included in the title separated with spaces. This constructor cannot be used as a copy constructor. Default values:
            nbins = 100
            low   = 0
            up    = 1
            title = 'h1' '''
                
        self.nbins = nbins
        self.low   = float( low )
        self.up    = float(  up )
        
        if len( tit.split() ) == 1:
            self.tit  = tit
            self.xtit = ''
            self.ytit = ''
        else:
            self.tit, self.xtit, self.ytit = tit.split()
        
        # Includes underflow and overflow bins
        self.data = dict( zip( [-float('inf')] + Binning( self.nbins, self.low, self.up ) + [ self.up ], Zeros( nbins + 2 ) ) )
    
    def __repr__(self):
        return StrDic( self.data )
    
    '''Quedei aqui.'''
    def GetBinOf( self, point ):
        for bin in Reversed( self.Bins() ):
            if valor>=bin:    def Fill( self, point, quantity = 1 ):
        for bin in invertir(self.Bins()):
            if valor>=bin:
                self.datos[bin] += cantidade
                break
    
    def importar(self,H):
        if not isinstance(H,TH1):
            argerro(self.importar)
        self = H1( H.GetNbinsX(),
                  H.GetXaxis().GetXmin(),
                  H.GetXaxis().GetXmax(),
                  H.GetTitle() + ' ' + H.GetXaxis().GetTitle() + ' ' + H.GetYaxis().GetTitle() )
        for i in range(nbins + 2 ):
            self.Fill(self.Bin(i)[0],H.GetBinContent(i))
    
    def Bin( self, n ):
        bin = self.Bins()[n]
        return bin,self.datos[bin]
    
    def N(self):
        return sum( self.Valores() )
    
    def __add__(self,other):
        if not self.bins==other.bins:
            return False
        map( Fill(self.Bin(i)[0], other.Bin(i)[1] ) )
        return self
    
    def Copia(self):
        
        histo = H1(self.nbins,
                   self.low,
                   self.up,
                   self.nome + ' ' + self.xtit + ' ' + self.ytit)
        for i in range(nbins + 2 ):
            histo.Fill(*self.Bin(i))
        return histo
    
    def Bins(self):
        return sorted(self.datos.keys())
    
    def Valores(self):
        return map( lambda x: self.datos[x], self.Bins() )
    
    def Media(self):
        return media( self.Bins()[1:-1],self.Valores()[1:-1] )
    
    def Mediana(self):
        return mediana( self.Bins()[1:-1],self.Valores()[1:-1] )
    
    def Moda(self):
        return invertir(sorted(zip(self.Valores(),self.Bins())))[0][1]
