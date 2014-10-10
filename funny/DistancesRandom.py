from ROOT import *
from Plots import *

R   = TRandom3(0)

def random():
    return R.Uniform(-1,1)#R.Gaus(0,1)

def norm( vector ):
    return sum( map( lambda x: x**2, vector ) )**.5

def get( ndim ):
    return norm( [ random() - random() for i in range(ndim) ] )

hdr1 = TH1D( 'dr1', 'Distance between two random points in 1 dim', 1000, 0, 10 )
hdr2 = TH1D( 'dr2', 'Distance between two random points in 2 dim', 1000, 0, 10 )
hdr3 = TH1D( 'dr3', 'Distance between two random points in 3 dim', 1000, 0, 10 )
hdr4 = TH1D( 'dr4', 'Distance between two random points in 4 dim', 1000, 0, 10 )
hdr5 = TH1D( 'dr5', 'Distance between two random points in 5 dim', 1000, 0, 10 )
hdr6 = TH1D( 'dr6', 'Distance between two random points in 6 dim', 1000, 0, 10 )

for i in xrange(100000):
    hdr1.Fill( get(1) )
    hdr2.Fill( get(2) )
    hdr3.Fill( get(3) )
    hdr4.Fill( get(4) )
    hdr5.Fill( get(5) )
    hdr6.Fill( get(6) )

c = PutInCanvas( (hdr1, hdr2, hdr3, hdr4, hdr5, hdr6 ) )
