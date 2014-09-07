from ROOT import *
from math import *
from check import *
from functions import binning,mean,median,mode

class matrix(vector):
    ''' Matrix instance. It is constructed by its components in a list of lists. Format row - column.'''
    
    def __init__( self, values, rowdim=0, coldim=0):
        ''' Class constructor. It takes the list of list and copy them to the data members.'''
        if not (rowdim==0 and coldim==0):
            self.__rows = rowdim
            self.__cols = coldim
            self.__v = vector( vector(values,coldim), rowdim )
        else:
            self.__v = vector(map( lambda x: vector(x), values ))
            self.__rows = len(self.__v)
            self.__cols = len(self.__v[0])
    
    def __add__( self, other ):
        ''' Sum operator with a number or another matrix.'''
        if not isinstance(other,matrix):
            other = matrix( other, self.__rows, self.__cols)
        return matrix( self.__v + other.__v )
    
    def __mul__( self, other ):
        ''' Product operator with a number or another matrix (component by component).'''
        if not isinstance(other,matrix):
            other = matrix( other, self.__rows, self.__rows )
        return matrix( self.__v * other.__v )
    
    def __pow__( self, other ):
        ''' Returns matrix product of the matrix with another matrix.'''
        return matrix( [ map( lambda x: self.__v[i]**x, other.trans().__m ) for i in range(self.__rows) ] )
    
    def __neg__( self ):
        ''' Parity operation on the matrix.'''
        return matrix( -self.__v )
    
    def __div__( self, other):
        ''' Division operation with a number or another matrix.'''
        if not isinstance(other,matrix):
            other = matrix( other, self.__rows, self.__rows )
        return self*(1./other)
    
    def __rdiv__( self, number ):
        ''' Operation defined for other classes when dividing by a matrix.'''
        return matrix(number*(1./self.__v))
        
    def __repr__(self):
        ''' Returns a string representation of the matrix.'''
        return reduce( lambda x,y: str(x) + '\n' + str(y), self.__v )

    def trans(self):
        other = matrix(self)
        return matrix([[other[j][i] for j in range(self.__rows)] for i in range(self.__cols)])

    def __getitem__(self,index):
        ''' Returns the index-th component of the vector starting from 0.'''
        return self.__v[index]

    def __setitem__(self,index,value):
        ''' Assign value to the index-th component of the vector.'''
        self.__v[index] = value

    def Zero( self ):
        ''' Sets all the coordinates to 0.'''
        self.__v = vector( vector(0,self.__cols), self.__rows )

    def __len__( self ):
        return self.__rows, self.__cols

class H1:
    def __init__(self,nbins=100,lower=0,upper=1,name='h1'):
        self.__nbins = nbins
        self.__lower = lower
        self.__upper = upper
        if len(name.split(' '))==1:
            self.__name = name
            self.__xtitle = ''
            self.__ytitle = ''
        else:
            self.__name,self.__xtitle, self.__ytitle = name.split(' ',name)
        self.__bins = zip(f.binning(nbins,lower,upper)+[upper],f.zeros(nbins+1))
    
    def __repr__(self):
        return reduce( lambda x,y: x+y, map( lambda x,y: str(x) + ' ' + str(y) + '\n', *zip(*self.__bins) ) )

    def Fill( self, value ):
        for i in range(1,len(self.__bins)):
            if value<self.__bins[i][0]:
                self.__bins[i-1] = ( self.__bins[i-1][0], self.__bins[i-1][1] + 1 )
    def SetBinContent(self,bin,N):
        self.__bins[bin] = ( self.__bins[bin][0], N)

    def root(self,H):
        if not isinstance(H,TH1):
            wrong(self.root)
        self.__nbins  = H.GetNbinsX()
        self.__lower  = H.GetXaxis().GetXmin()
        self.__upper  = H.GetXaxis().GetXmax()
        self.__bins   = zip(binning(self.__nbins,self.__lower,self.__upper)+[self.__upper],f.zeros(self.__nbins+1))
        self.__name   = H.GetTitle()
        self.__xtitle = H.GetXaxis().GetTitle()
        self.__ytitle = H.GetYaxis().GetTitle()
        for i in range(self.__nbins):
            self.SetBinContent(i,H.GetBinContent(i+1))
    def Xtitle(self):
        return self.__xtitle
    def Ytitle(self):
        return self.__ytitle
    def Name(self):
        return self.__name
    def Title(self):
        return self.__name
    def GetBin( self,index ):
        return self.__bins[index]
    def GetTotalEntries(self):
        return sum( self.GetEntries )
    def __add__(self,other):
        selfbins,selfvalues = zip(*self.__bins)
        otherbins,othervalues = zip(*other.__bins)
        if not selfbins==otherbins:
            return False
        map( lambda i: self.SetBinContent(i,self.__bins[i][1] + other.__bins[i][1]), range(self.__nbins) )
    def copy(self):
        other = H1()
        other.__nbins  = self.__nbins
        other.__lower  = self.__lower
        other.__upper  = self.__upper
        other.__bins   = zip(self.GetBins(),self.GetEntries())
        other.__name   = self.Name()
        other.__xtitle = self.Xtitle()
        other.__ytitle = self.Ytitle()
        map( lambda i: other.SetBinContent(i,self.__bins[i][1]), range(self.__nbins) )
        return other
    def GetBins(self):
        return zip(*self.__bins)[0]
    def GetEntries(self):
        return zip(*self.__bins)[1]
    def Mean(self):
        return mean( self.__bins )
    def Median(self):
        return median( self.__bins )
    def Mode(self):
        return mode( self.__bins )

class Ntuple(dict):
    def __init__(self,*variables):
        self.__data={}
        for v in variables:
            self.__data[v] = []
    def __add__(self,other):
        if not self.__data.keys()==other.__data.keys():
            wrong(self.__add__)
        result = Ntuple()
        result.__data = dict( zip(self.__data.keys(),  map(lambda x,y: x+y, self.__data.values(), other.__data.values() ) ) )
        return result
    def __pow__(self,other):
        result = Ntuple()
        result.__data = dict( zip( self.__data.keys() + other.__data.keys(), self.__data.values() + other.__data.values() ) )
        return result
    def __repr__(self):
        return reduce( lambda x,y: x+y, map( lambda x,y: str(x) + ' ' + str(y) + '\n', *zip(*self.__data.items()) ) )
    def GetEvent(self,N):
        return dict( zip(self.__data.keys(), map( lambda x: x[N],self.__data.values() ) ) )
    def GetEvents(self):
        return self.__data
    def GetVar(self,var):
        return self.__data[var]
    def Add(self, data):
        for var,val in data.items():
            self.__data[var] += [val]

h = H1()
H = TH1F('h','h',100,0,1)
H.Fill(0.4)
H.Fill(0.98)
H.Fill(0.71)
h.root(H)



a = Complex(1,2)
b = Complex(9,8.)
c = Complex(0,1)
v = vector([1,2,3])
w = vector([5,5,5])
z = vector([0,0,1])

m = matrix( [ [1,2], [3,4] ] )
n = matrix( [ [4,3], [2,1] ] )