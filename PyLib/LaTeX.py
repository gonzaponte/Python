# -*- coding: utf-8 -*-
#
# Module with some useful functions to create LaTeX documents.
# Note: not updated, not checked.
#
# Author: Gonzalo Martinez
#
# Last update: --/--/--
#

from math import log10
from Math import Sign
from General import rint, fint
import os


def MakeTable( *columns ):
    return r'''
\begin{table}
\begin{center}
\begin{tabular}{''' + '|'.join( ['c'] * len(columns) ) + r'''} \hline
''' + ''.join( map( lambda row: ' & '.join( map(str,row) ) + r''' \\ \hline
''', zip( *columns ) ) )+r'''
\end{tabular}
\end{center}
\end{table}'''

def Ndigits( x, N = 2 ):
    '''Returns the number with the number of significant digits specified.'''
    return round( x, N - int( log10(abs(x)) ) ) if abs(x) < 1 else round( x, N - int( log10(abs(x)) ) - 1 )

def SetError( x, sx, exponent = 'auto' ):
    s  = Sign(  x )
    x  =  abs(  x )
    sx =  abs( sx )

    xexp = fint( log10(  x ) )
    sexp = fint( log10( sx ) ) - 1
    sx   = rint( sx * 0.1**sexp )
    x    = Ndigits( x, xexp - sexp + 1 )
    x   *= 0.1 ** xexp if exponent == 'auto' else 0.1 ** exponent
    xexp = exponent if not exponent == 'auto' else xexp

    return '{0}({1}) \\cdot 10$^'.format(x,sx) + '{' + str(xexp) + '}$ ' if xexp else '{0}({1}) '.format( x, sx )

def MakeFigures( figures, format = '.pdf', folder = './', properties = '' ):
    return '\n'.join( map( lambda figure: r'''
\begin{figure}
\centering
\includegraphics[''' + properties + r''']{''' +  folder + figure + format + r'''}
\end{figure}''', figures ) )

def MakeLaTeX( text, file, append = False ):
    f = file.open( file, 'w' ) if not append else file.open( file, 'a' )
    f.write( text )
    f.close()
    os.system( 'pdflatex ' + file )
    os.system( 'open '     + file )











