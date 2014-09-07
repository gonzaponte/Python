#
# Module that contains useful plotting functions (using ROOT)
#
#
# Author: Gonzalo Martinez
#
# Last update: 17 / 03 / 2014
#

import os
from ROOT import gStyle, TCanvas, TGraph, TGraphErrors, TFile, TProfile, TH1F, TTree
from array import array
from Sequences import Zeros
from math import sqrt
from numpy import array as narray
import PIL.Image as pili
from images2gif import *


Colors = [   4,   2,   1,  53,   8,
            95,  14,   7, 205,   3,
           218,   6,  46,  40,   5] * 100

canvasorganization = {}
canvasorganization[1] = ( 1, 2 )
canvasorganization[2] = ( 1, 2 )
canvasorganization[3] = ( 2, 2 )
canvasorganization[4] = ( 2, 2 )
canvasorganization[5] = ( 2, 3 )
canvasorganization[6] = ( 2, 3 )
canvasorganization[7] = ( 3, 3 )
canvasorganization[8] = ( 3, 3 )
canvasorganization[9] = ( 3, 3 )

def printcolortable():
    ''' Prints the color table that which is used when plots are merged.'''
    
    from ROOT import TH1I
    COLORS = Colors[:15]
    NofC = len(COLORS)
    
    c = TCanvas()
    h = [ TH1I( 'colortable' + str(i), 'Color table', NofC, 0, NofC ) for i in range(NofC) ]
    
    gStyle.SetOptStat('')
    map( lambda i, c: h[i].SetFillColor(c)                     , range(NofC), COLORS )
    map( lambda hist: hist.GetXaxis().SetNdivisions(NofC,False), h )
    map( lambda hist: hist.GetYaxis().SetLabelColor(0), h )
    map( lambda hist: hist.GetYaxis().SetTickLength(0), h )
    map( lambda hist: hist.SetMaximum(1), h )
    
    for i in range(NofC):
        h[i].Fill(i)
        h[i].Draw('same')

    return c,h

def Graph( x, y, xaxis='', yaxis='',title='', markerstyle = None, markersize = None ):
    ''' Returns a TGraph made of x,y data with optional titles.'''

    if not len(x) == len(y):
        raise ValueError('Both data lists must have the same length.')
    
    graph = TGraph( len(x), array('f',x), array('f',y) )

    if xaxis:
        graph.GetXaxis().SetTitle( xaxis )
    if yaxis:
        graph.GetYaxis().SetTitle( yaxis )
    if title:
        graph.SetTitle( title )
    if markerstyle:
        graph.SetMarkerStyle( markerstyle )
    if markersize:
        graph.SetMarkerSize( markersize )

    return graph

def ErrorsGraph( x, y, ex, ey, xaxis='', yaxis='',title='' ):
    ''' Returns a TGraphErrors made of x,y data with optional titles.'''
    
    if ex is None:
        ex = Zeros( len(x) )

    if not len(x) == len(y) == len(ex) == len(ey):
        raise ValueError('Both data lists must have the same length.')

    graph = TGraphErrors( len(x), array('f',x), array('f',y), array('f',ex), array('f',ey) )
    
    if xaxis:
        graph.GetXaxis().SetTitle( xaxis )
    if yaxis:
        graph.GetYaxis().SetTitle( yaxis )
    if title:
        graph.SetTitle( title )
    
    return graph


def GetMax( histogram ):
    ''' Returns the value of the bin with the greatest value.'''
    
    return histogram.GetBinContent( histogram.GetMaximumBin() )

def Norm2integral( histogram ):
    ''' Scales the histogram so that the integral is 1.'''
    
    histogram.Scale( 1./ histogram.Integral() )
    return histogram

def Norm2maximum( histogram ):
    ''' Scales the histogram so that the greatest bin is setted to 1.'''
    
    histogram.Scale( 1./ GetMax( histogram ) )
    return histogram

def Merge1D( histograms, xaxis = '', yaxis = '', title = '' ):
    ''' Draws in the same canvas all the histograms passed. Returns the canvas.'''
    
    c = TCanvas()
    
    for i in range( len(histograms) ):
        h = histograms[i]
        h.SetLineColor( Colors[i] )
        h.Draw( 'SAME' )

    histograms[0].SetMaximum( max( map( GetMax, histograms ) ) )

    if xaxis:
        histograms[0].GetXaxis().SetTitle( xaxis )
    if yaxis:
        histograms[0].GetYaxis().SetTitle( yaxis )
    if title:
        histograms[0].SetTitle( title )

    return c

def Gethisto( file, hname ):
    ''' Gets an histogram from a file. It accepts the name of the file or the file itself. Use this last option when getting a lot of histograms from the same file.'''
    
    if isinstance( file, str ):
        file = TFile( file )

    h = file.Get( hname )
    if isinstance( h, TProfile ):
        h.SetErrorOption('')
    
    return h

def Addprofile( h2, hp, color = 2, width = 3 ):
    ''' Merges the scatter plot with its profile. Returns the canvas.'''
    
    c = TCanvas()
    h2.Draw()
    hp.Draw('SAME')
    hp.SetLineColor( color )
    hp.SetLineWidth( width )
    
    return c


def makepresentation( histograms, directory, texfile = 'Presentation' ):
    ''' Makes a beamer presentation with the histograms passed. Directory is the folder where the images are stored.'''
    
    header=r'''
        \documentclass{beamer}
        \usetheme{default}
        \begin{document}
        '''
    
    ending=r'''
        \end{document}'''
    
    frame1=r'''
        \begin{frame}
        \begin{figure}
        \centering
        \includegraphics[scale=0.55]{'''
    
    frame2=r'''}
        \end{figure}
        \end{frame}'''
    
    f = open( texfile + '.tex', 'w' )
    f.write( header )
    
    for name in histograms:
        f.write( frame1 )
        f.write( directory + name )
        f.write( frame2 )
    
    f.write( ending )
    f.close()

    os.system( 'pdflatex ' + texfile + '.tex')
    os.system( 'rm -f *.toc')
    os.system( 'rm -f *.aux')
    os.system( 'rm -f *.log')
    os.system( 'rm -f *.nav')
    os.system( 'rm -f *.out')
    os.system( 'rm -f *.snm')
    os.system( 'open ' + texfile + '.pdf' )
    
    return None

def Sumhistos( *hlist ):
    ''' Sums the histograms.'''
    
    if not isinstance( hlist, (list,tuple) ):
        hlist = [ hlist ]
    
    H = hlist[0]
    for h in hlist[1:]:
        H.Add( h )

def GoodLooking( histogram, color = 1, width = 2, fill = None ):
    ''' Sets the usual attributer to the histogram for a fancy presentation.'''
    
    histogram.SetLineColor( color )
    histogram.SetLineWidth( width )
    if fill:
        histogram.SetFillColor( fill )

def MakeH1( data, title = 'histo', nbins = 100 ):
    ''' Returns the distribution of data.'''
    
    Data = sorted( data )
    if isinstance( data[0], (tuple) ):
        nbins = len( Data )
        MIN   = Data[0][0]
        MAX   = Data[-1][0]
        MAX  += ( MAX - MIN ) / ( nbins - 1 )
        histo = TH1F( title, title, nbins, MIN, MAX )
        [ histo.SetBinContent( i + 1, data[i][1] ) for i in range( nbins ) ]
    else:
        MIN  = Data[ 0]
        MAX  = Data[-1]
        MAX += ( MAX - MIN ) / ( nbins - 1 )
        histo = TH1F( title, title, nbins, MIN, MAX )
        map( histo.Fill, data )
    
    return histo
    
def PutInCanvas( objects, Options = None, nhorizontal = None, nvertical = None ):
    if nhorizontal is None and nvertical is None:
        nhorizontal, nvertical = canvasorganization[ len(objects) ]

    if Options is None:
        Options = [''] * len( objects )
    
    c = TCanvas()
    c.Divide( nhorizontal, nvertical )

    for i in range(len(objects)):
        c.cd(i+1)
        objects[i].Draw( Options[i] )

    return c

def Plot4D( x, y, z, t, markerstyle = 20, markersize = 1 ):
    data = narray( [0.] * 4 )
    tree = TTree('DummyTree','DummyTree')
    tree.Branch('xyzt', data, 'x/D:y:z:t')

    for datai in zip(x,y,z,t):
        data[0], data[1], data[2], data[3] = datai
        #print data
        tree.Fill()
    tree.SetMarkerStyle( markerstyle )
    tree.SetMarkerSize( markersize )
    c = TCanvas()
    tree.Draw('x:y:z:t','','zcol')
    return c, tree

def MakeGif( names, directory = './', extension = '.png', frametime = 0.15, nloops = True, output = './GIF' ):
    images = [ pili.open( directory + name + extension ) for name in names ]
    writeGif( output + '.gif', images, frametime, nloops )

'''
from math import sqrt,log,exp
from scipy.interpolate import *

z = range( 11 )
x = [ -1, 0, 2, 1, -2, 0, 1, 1, 2, 0, 0 ]
y = x[::-1]
E = [ 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3 ]

xint = interp1d( z, x, 4, bounds_error = False, fill_value = 0. )
yint = interp1d( z, y, 4, bounds_error = False, fill_value = 0. )
Eint = Rbf(x,y,z,E)

znew = [ 0.01*i for i in range(1000)]
xnew = xint(znew)
ynew = yint(znew)
Enew = Eint(xnew,ynew,znew)

a = Plot4D( x, y, z, E )
b = Plot4D( xnew, ynew, znew, Enew )
'''