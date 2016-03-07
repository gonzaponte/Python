#
# Module that contains useful plotting functions (using ROOT)
#
#
# Author: Gonzalo Martinez
#
# Last update: 17 / 03 / 2014
#

import os
import ROOT
import array
import Sequences
try:
    import PIL.Image
    import images2gif
except:
    print 'Modules PIL and images2gif not found'


_colors = [   4,   2,   1,  53,   8,
              7,  14,  95, 205,   3,
            218,   6,  46,  40,   5] * 100

_canvasorganization     = {}
_canvasorganization[1]  = ( 1, 0 )
_canvasorganization[2]  = ( 1, 2 )
_canvasorganization[3]  = ( 2, 2 )
_canvasorganization[4]  = ( 2, 2 )
_canvasorganization[5]  = ( 2, 3 )
_canvasorganization[6]  = ( 2, 3 )
_canvasorganization[7]  = ( 3, 3 )
_canvasorganization[8]  = ( 3, 3 )
_canvasorganization[9]  = ( 3, 3 )
_canvasorganization[10] = ( 2, 5 )

def PrintColorsTable():
    '''
        Draw the colors table that is used when some plots are merged.
    '''
    Ncol   = 15
    
    c = ROOT.TCanvas()
    h = [ ROOT.TH1I( 'colortable' + str(i), 'Color table', Ncol, 0, Ncol ) for i in range(Ncol) ]
    
    ROOT.gStyle.SetOptStat('')
    map( lambda hi, c: hi.SetFillColor(c), h, _colors[:15] )
    map( lambda hi:    hi.GetXaxis().SetNdivisions(NofC,False), h )
    map( lambda hi:    hi.GetYaxis().SetLabelColor(0),          h )
    map( lambda hi:    hi.GetYaxis().SetTickLength(0),          h )
    map( lambda hi:    hi.SetMaximum(1),                        h )
    
    for i in range(Ncol):
        h[i].Fill(i)
        h[i].Draw('same')

    return c,h

def Graph( x, y, xaxis='', yaxis='',title='', markerstyle = None, markersize = None, markercolor = None ):
    '''
        Returns a TGraph made of x,y data with optional titles.
    '''

    assert len(x) == len(y), ValueError('Both lists must have the same length.')
    
    graph = ROOT.TGraph( len(x), array.array('f',x), array.array('f',y) )

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
    if markercolor:
        graph.SetMarkerColor( markercolor )
        graph.SetLineColor( markercolor )

    return graph

def Graph2( x, y, z, xaxis='', yaxis='', zaxis = '', title='', markerstyle = None, markersize = None, markercolor = None ):
    '''
        Returns a TGraph2D made of x,y,z data with optional titles.
    '''
    
    assert len(x) == len(y) == len(z), ValueError('Both lists must have the same length.')
    
    graph = ROOT.TGraph2D( len(x), array.array('f',x), array.array('f',y), array.array('f',z) )
    
    if xaxis:
        graph.GetXaxis().SetTitle( xaxis )
    if yaxis:
        graph.GetYaxis().SetTitle( yaxis )
    if zaxis:
        graph.GetZaxis().SetTitle( zaxis )
    if title:
        graph.SetTitle( title )
    if markerstyle:
        graph.SetMarkerStyle( markerstyle )
    if markersize:
        graph.SetMarkerSize( markersize )
    if markercolor:
        graph.SetMarkerColor( markercolor )
        graph.SetLineColor( markercolor )


    return graph

def ErrorsGraph( x, y, ex, ey, xaxis='', yaxis='',title='' ):
    '''
        Returns a TGraphErrors made of x,y data with optional titles.
    '''

    ex = Sequences.Zeros( len(x) ) if ex is None else ex

    assert len(x) == len(y) == len(ex) == len(ey), ValueError('Data lists must have the same length.')

    graph = ROOT.TGraphErrors( len(x), array.array('f', x), array.array('f', y),
                                       array.array('f',ex), array.array('f',ey) )
    
    if xaxis:
        graph.GetXaxis().SetTitle( xaxis )
    if yaxis:
        graph.GetYaxis().SetTitle( yaxis )
    if title:
        graph.SetTitle( title )
    
    return graph

def GetMax( histogram ):
    '''
        Returns the value of the bin with the greatest value.
        '''
    
    return histogram.GetBinContent( histogram.GetMaximumBin() )

def GetMin( histogram ):
    '''
        Returns the value of the bin with the smallest value.
    '''
    
    return histogram.GetBinContent( histogram.GetMinimumBin() )

def Norm2integral( histogram ):
    '''
        Scales the histogram so that the integral is 1.
    '''
    
    histogram.Scale( 1./ histogram.Integral() )
    return histogram

def Norm2maximum( histogram ):
    ''' 
        Scales the histogram so that the greatest bin is setted to 1.
    '''
    
    histogram.Scale( 1./ GetMax( histogram ) )
    return histogram

def Merge1D( histograms, xaxis = '', yaxis = '', title = '' ):
    '''
        Draws in the same canvas all the histograms passed. Returns the canvas.
    '''
    
    c = ROOT.TCanvas()
    
    for i in range( len(histograms) ):
        h = histograms[i]
        h.SetLineColor( _colors[i] )
        h.Draw( 'SAME' )

    histograms[0].SetMaximum( max( map( GetMax, histograms ) ) )
    histograms[0].SetMinimum( min( map( GetMin, histograms ) ) )

    if xaxis:
        histograms[0].GetXaxis().SetTitle( xaxis )
    if yaxis:
        histograms[0].GetYaxis().SetTitle( yaxis )
    if title:
        histograms[0].SetTitle( title )

    return c

def Gethisto( file, hname ):
    '''
        Gets an histogram from a file. It accepts the name of the file or the file itself. Use the latter option when getting a lot of histograms from the same file.
    '''
    
    if isinstance( file, str ):
        file = ROOT.TFile( file )

    h = file.Get( hname )
    if isinstance( h, ROOT.TProfile ):
        h.SetErrorOption('')
    
    return h

def Addprofile( h2, hp, color = 2, width = 3 ):
    '''
        Merges the scatter plot with its profile. Returns the canvas.
    '''
    
    c = ROOT.TCanvas()
    h2.Draw()
    hp.Draw('SAME')
    hp.SetLineColor( color )
    hp.SetLineWidth( width )
    
    return c


def makepresentation( histograms, directory, texfile = 'Presentation' ):
    '''
        Makes a beamer presentation with the histograms passed. Directory is the folder where the images are stored.
    '''
    
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
    '''
        Sums the histograms.
    '''
    
    H = hlist[0]
    for h in hlist[1:]:
        H.Add( h )

def GoodLooking( histogram, color = 1, width = 2, fill = None ):
    '''
        Sets the usual attributer to the histogram for a fancy presentation.
    '''
    
    histogram.SetLineColor( color )
    histogram.SetLineWidth( width )
    if fill:
        histogram.SetFillColor( fill )

def MakeH1( data, title = 'histo', nbins = 100 ):
    '''
        Returns the distribution of data.
    '''
    
    Data = sorted( data )
    if isinstance( data[0], tuple ):
        nbins = len( Data )
        MIN   = Data[0][0]
        MAX   = Data[-1][0]
        MAX  += ( MAX - MIN ) / ( nbins - 1 )
        histo = ROOT.TH1F( title, title, nbins, MIN, MAX )
        [ histo.SetBinContent( i + 1, data[i][1] ) for i in range( nbins ) ]
    else:
        MIN  = Data[ 0]
        MAX  = Data[-1]
        MAX += ( MAX - MIN ) / ( nbins - 1 )
        histo = ROOT.TH1F( title, title, nbins, MIN, MAX )
        map( histo.Fill, data )
    
    return histo
    
def PutInCanvas( objects, Options = None, nhorizontal = None, nvertical = None, canvassize= None ):
    '''
        Draw each object in a subcanvas.
    '''
    if nhorizontal is None and nvertical is None:
        nhorizontal, nvertical = _canvasorganization[ len(objects) ]

    if Options is None:
        Options = [''] * len( objects )
    
    c = ROOT.TCanvas() if canvassize is None else ROOT.TCanvas('canvas','',canvassize[0],canvassize[1])
    c.Divide( nhorizontal, nvertical )

    for i in range(len(objects)):
        c.cd(i+1)
        objects[i].Draw( Options[i] )

    return c

def FromH3( histo ):
    '''
        Get the data from a 3D histogram as a set x,y,z,entries.
    '''
    data = []
    for i in range(1,histo.GetNbinsX()+1):
        for j in range(1,histo.GetNbinsY()+1):
            for k in range(1,histo.GetNbinsZ()+1):
                x = histo.GetXaxis().GetBinCenter(i)
                y = histo.GetYaxis().GetBinCenter(j)
                z = histo.GetZaxis().GetBinCenter(k)
                N = histo.GetBinContent(i,j,k)
                data.append( (x, y, z, N) )
    return data

def Plot4D( x, y, z, t, markerstyle = 20, markersize = 1 ):
    '''
        Plot a 3D dataset (x,y,z) with an extra color coordinate (t).
    '''
    data = array.array( 'd', [0.] * 4 )
    tree = ROOT.TTree('DummyTree','DummyTree')
    tree.Branch('xyzt', data, 'x/D:y:z:t')

    for datai in zip(x,y,z,t):
        data[0], data[1], data[2], data[3] = datai
        tree.Fill()
    tree.SetMarkerStyle( markerstyle )
    tree.SetMarkerSize( markersize )
    c = ROOT.TCanvas()
    tree.Draw('x:y:z:t','','zcol')
    return c, tree

def MakeGif( names, directory = './', extension = '.png', frametime = 0.15, nloops = True, output = './GIF' ):
    '''
        Create a gif file with images in directory directory and names names.
    '''
    images = [ PIL.Image.open( directory + name + extension ) for name in names ]
    images2gif.writeGif( output + '.gif', images, frametime, nloops )
