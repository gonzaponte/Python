from ROOT import *
from math import *
from RandomNumbers import RandomChoice

R1 = TRandom3()
R1.SetSeed(0)

R2 = TRandom3()
R2.SetSeed(0)


def RChoice1():
    return round( R1.Uniform(-1.5,1.5) )

def RChoice2():
    return round( R2.Uniform(-1.5,1.5) )

RChoice = RandomChoice( (0,0), (1,0), (0,1), (0,-1), (-1,0) )

def Enumerator( N0 ):
    N = N0 - 1
    while True:
        N += 1
        yield N

def Graph():
    J = TGraph()
    J.SetMarkerStyle(20)
    J.SetMarkerSize(.8)
    return J

def Line( maxpoints = 100000 ):
    x  = 0
    Gx = Graph()
    Gr = Graph()
    for n in xrange( maxpoints ):
        dr = RChoice()
        x += dr
        Gx.SetPoint( n, n, x )
        Gr.SetPoint( n, n, abs(x) )
    
    return Gx, Gr


def Square( maxpoints = 100000, show = True ):
    x = y = 0
    Gxy = Graph()
    Gtr = Graph()
    if show:
        c = TCanvas()
        c.Divide(1,2)
    
    for n in xrange( maxpoints ):
        dx = RChoice1()
        dy = RChoice2() if dx else 0.
        x += dx
        y += dy
        Gxy.SetPoint( n, x, y )
        Gtr.SetPoint( n, n, sqrt( x**2 + y**2 ) )
    
        if show:
            c.cd(1)
            Gxy.Draw('APC')
            c.cd(2)
            Gtr.Draw('APC')
            c.Update()

    return Gxy, Gtr

def Square( maxpoints = 100000, show = True ):
    x = y = 0
    Gxy = Graph()
    Gtr = Graph()
    if show:
        c = TCanvas()
        c.Divide(1,2)
    
    for n in xrange( maxpoints ):
        dx, dy = RChoice.Get()
        x += dx
        y += dy
        Gxy.SetPoint( n, x, y )
        Gtr.SetPoint( n, n, sqrt( x**2 + y**2 ) )
        
        if show:
            c.cd(1)
            Gxy.Draw('APL')
            c.cd(2)
            Gtr.Draw('APC')
            c.Update()
    
    return Gxy, Gtr


#gxy, gtr = Line()
gxy, gtr = Square()

#c = TCanvas()
#c.Divide(1,2)
#c.cd(1)
#gxy.Draw('APC')
#c.cd(2)
#gtr.Draw('APC')
