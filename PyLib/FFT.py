'''
    Contains tools related to Fast Fourier Transforms.
'''
import math
import Array
import Plots
import numpy.fft
import time
import Time
import copy

def ZeroPadding( data ):
    N  = len(data)
    N2 = math.log( N, 2 )
    if not N2 == int(N2):
        data.extend( [0.] * ( 2**(int(N2)+1) - N ) )
    return data

def SlowFFT1( data ):
    N = len(data)
    twopiN = -2. * math.pi / N
    W      = complex( math.cos( twopiN ), math.sin( twopiN ) )
    return list( Array.Matrix( [ [ W**(n*k) for k in range(N)] for n in range(N) ] ) ** Array.Vector(data) )

def FFT1( data ):
    N = len( data )
    if N is 1:
        return data
    #else
    fdata  = [0.] * N
    twopiN = -2. * math.pi / N
    W      = complex( math.cos( twopiN ), math.sin( twopiN ) )

    feven, fodd = map( FFT1, (data[::2], data[1::2]) )
    for k in range(N//2):
        Wk = W**k
        fdata[k       ] = feven[k] + Wk * fodd[k]
        fdata[k + N//2] = feven[k] - Wk * fodd[k]
    
    return fdata

def VFFT1( data, Nmin = 32 ):
    N      = len( data )
    Left   = N // Nmin
    twopiN = -2. * math.pi / Nmin
    W      = complex( math.cos( twopiN ), math.sin( twopiN ) )
    
    M      = Array.Matrix( [ [ W**(n*k) for k in range(Nmin)] for n in range(Nmin) ] )
    X      = Array.Matrix( [ data[i:i+Left] for i in range(0,N,Left) ] )
    F      = M ** X
    F      = F.T()
    twopiN = -1. * math.pi / Nmin
    W      = complex( math.cos( twopiN ), math.sin( twopiN ) )
    Wk     = Array.Vector( [W**k for k in range(Nmin) ] )
    fdata  = list(F[0] + Wk * F[1]) + list(F[0] - Wk * F[1])
    
    return fdata

def FFT2( data ):
    fdata = Array.Matrix(data)
    for N in fdata.Size():
        for i in range(N):
            fdata[i] = Array.Vector( FFT1( fdata[i] ) )
        fdata = fdata.T()

    return fdata.ToList()

def Shift1( data ):
    N = len(data)
    return data[N//2:] + data[:N//2]

def Shift2( data ):
    newdata = copy.deepcopy(data)
    for i in range(2):
        newdata = Array.Matrix( map( Shift1, newdata ) ).T().ToList()
    return newdata

def plot(data):
    c = Plots.ROOT.TCanvas()
    g = Plots.Graph( range(len(data)), data, markerstyle = 20, markersize = 1 )
    g.Draw('AP')
    return c,g

def plot2(data):
    c = Plots.ROOT.TCanvas()
    x = [ [ i ] * len(data) for i in range(len(data)) ]
    y = [ range(len(data))  for i in range(len(data)) ]
    x = reduce( lambda a,b: a+b, x )
    y = reduce( lambda a,b: a+b, y )
    z = reduce( lambda a,b: a+b, data )
    g = Plots.Graph2( x, y, z, markerstyle = 20, markersize = 1 )
    g.Draw('zcol')
    c.Update()
    return c,g

if __name__ == '__main__':
    '''
    data = [ 1. if i==32 else 0. for i in range(64) ]
    data = [ math.exp(-i**2/200.) for i in range(-32,32) ]
    fdata = map(abs,FFT1(data))
    sdata = map(abs,SlowFFT1(data))
    vdata = map(abs,VFFT1(data))
    a = plot(data)
    b = plot(Shift1(fdata))
    c = plot(Shift1(sdata))
    d = plot(Shift1(vdata))
    '''

    data2 = [[1. if i == j == 32 else 0. for j in range(64)] for i in range(64) ]
    data2 = [[ math.exp(-(x**2+y**2)/2.) for y in range(-32,32)] for x in range(-32,32)]
#    data2[
    fdata2 = map(lambda x:map(abs,x),FFT2(data2))
    e     = plot2(data2)
    f     = plot2(Shift2(fdata2))
