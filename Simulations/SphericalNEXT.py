from ROOT import *
from math import *

R = TRandom2(0)

Nsipms = 100
hsipms = TH2I( 'hsipms', '', 1000, -1, 1, 1000, 0, 2*pi )

def Fibbo():
    a0 = 0.5*(1+5**0.5) - 1
    a1 = a0 * 2*pi
    poss = []
    for i in range(1, Nsipms + 1):
        phi = ( a1 * i ) % (2*pi)
        theta = asin( i*2.0/Nsipms - 1.0 )
        hsipms.Fill(theta,phi)
        x = sin(theta) * cos(phi)
        y = sin(theta) * sin(phi)
        z = cos(theta)
        poss.append( (x,y,z) )
    return poss

def Grid():
    for i in range(int(Nsipms**0.5)):
        theta = acos( 1 - 2*i/Nsipms**0.5 )
        for j in range(int(Nsipms**0.5)):
            phi = j*2*pi/Nsipms**0.5
        

def Dists( poss ):
    dists = []
    for i in range(Nsipms):
        dists.append(float('inf'))
        for j in range(Nsipms):
            if i==j: continue
            d = sqrt( ( poss[j][0] - poss[i][0] )**2 + ( poss[j][1] - poss[i][1] )**2 + ( poss[j][2] - poss[i][2] )**2 )
            if d<dists[-1]:
                dists[-1] = d
                
    print dists


hdet = hsipms.Clone()
Fibbo()

for i in range(int(1e8)):
    theta = acos( R.Uniform(-1,1) )
    phi   = R.Uniform(0,2*pi)
    if hsipms.GetBinContent( hsipms.FindBin(theta,phi) ):
        hdet.Fill(theta,phi)
    
c = [TCanvas()]
hsipms.Draw('zcol')
c.append(TCanvas())
hdet.Draw('zcol')
raw_input()
    
