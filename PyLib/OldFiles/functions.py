import sys
from math import *
from check import *

def factorial( N ):
    ''' Returns x factorial.'''
    
    if not isint( N ) or N < 0:
        wrong(factorial)
    
    if N:
        return N * factorial( N - 1 )
    return 1

def doublefactorial( N ):
    ''' Returns x double factorial.'''

    if not isint( N ):
        wrong(doublefactorial)

    if N < 2:
        return 1
    return N * doublefactorial( N - 2 )

def zeros( rows, cols=0 ):
    ''' This function makes a vector (matrix) of size rows ( rows x cols ) filled with zeros.'''
    
    if not isint(rows) or not isint(cols):
        wrong(zeros)
    
    if not cols:
        return [0. for i in range(rows)]
    else:
        return [ zeros(cols) for i in range(rows) ]

def ones( rows, cols=0 ):
    ''' This function makes a vector (matrix) of size rows ( rows x cols ) filled with ones.'''
    
    if not isint(rows) or not isint(cols):
        wrong(ones)
    
    if not cols:
        return [1. for i in range(rows)]
    else:
        return [ ones(cols) for i in range(rows) ]

def identity( N ):
    ''' This functions returns an identity matrix of size N x N.'''
        
        M = zeros( N, N )
    for i in range( N ):
		M[i][i]=1.0
    
    return M

def Scale( M, F ):
    ''' This function takes a vector or a matrix of numbers and re-scale it by a factor F.'''
    
    if not iscontainer(M[0]):
        return map( lambda y: y*F, M )
    
    return map( lambda x: Scale(x,F), M )

def printmatrix( M ):
    ''' This function prints a matrix in a more visual form.'''
    
    for line in M:
        print line
    return None

def Order( L, number=0 ):
    ''' This function orders a list by its distance to a given number.'''

    return list( zip( *sorted( zip( map( lambda x: abs(x-number), L ), L ) ) )[1])


def Reverse( L ):
    ''' This function reverses the order of a list without destroying the original.'''

    return L[::-1]

def Izip( Z ):
    ''' This function inverts the zipping in a list of pairs without destroying the original.'''
    
    return zip( Reverse( zip( *Z ) ) )

def Asymmetry( x, y ):
    ''' This function returns the asymmetry factor between two values.'''
    
    return ( x - y )/float( x + y )

def MaxIndex( x ):
    ''' This function returns the index of the greatest value in a list.'''

    return x.index( max( x ) )

def MinIndex( x ):
    ''' This function returns the index of the smallest value in a list.'''

    return x.index( min(x) )

def Cumulative( L ):
    ''' This function return the cumulative of a given list.'''
    
    return [ sum( L[ :(i+1) ] ) for i in range( len(L) ) ]

def sign( x ):
    ''' Sign function.'''
    
    if x<0:
        return -1
    return 1

def MxM( M1, M2 ):
    ''' This function performs a matrix product between M1 and M2.'''
    
    rows1 = len( M1 )
    cols1 = len( M1[0] )
    cols2 = len( M2[0] )
    
    M = zeros( rows1, cols2 )
    
    for i in range(rows1):
        for j in range(cols2):
            for k in range(cols1):
                M[i][j]+= a[i][k]*b[k][j]
    return M

def transpose( M ):
    ''' Performs matrix transpose.'''
    
    return [ M[j][i] for i in range(len(M)) for j in range(M[0]) ]

def Diagonalize( M, p = 1e-8 ):
    ''' This function performs the diagonalization of a matrix using Jacobi algorith.'''
    
    def findmax(MM):
        maximum = 0.
        maxpos  = [0,0]
        for i in range(len(MM)):
            for j in range(len(MM[0])):
                if i==j:
                    continue
                if abs(MM[i][j]) > maximum:
                    maximum = abs(MM[i][j])
                    maxpos  = [i,j]
        return maxpos
    
    def check( M1, M2 ):
        for i in range(len(M1)):
            for j in range(len(M1[0])):
                if abs( M1[i][j] - M2[i][j] ) > p:
                    return False
        return True
    
    D = list( M )
    V = identity( len(M) )
    
    while True:
        row,col = findmax(D)
        t = ( D[col][col] - D[row][row] )/( 2.*D[row][col] )
        t = sign( t )/( abs(t) + math.sqrt( t**2 + 1 ) )
        c  = 1./math.sqrt( t**2 + 1 )
        s  = c * t
        R = identity( len(M) )
        R[row][row] =  c
        R[col][col] =  c
        R[row][col] =  s
        R[col][row] = -s
        DD = mxm( transpose( R ), mxm( D, R ) )
        VV = mxm( V, R )
        if check(D,DD) and check(V,VV):
            break
        D = DD
        V = VV
    return D,V

def Frecs( L ):
    ''' This function takes a list and returns a dictionary with the frecuency of each element.'''
    
    l = list(L)
    frecs={}
    
    for element in l:
        n = l.count(element)
        frecs[element] = n
        
        for i in range(n):
            l.remove(element)
    
    return frecs

def wait():
    ''' Debugging function.'''
    raw_input('waiting...')

def Binning( nbins = 100, lower = 0., upper = 1.):
    ''' This function returns a inverval sliced in several partitions (bins). The return is a list which values are the beginning of each bin. The arguments are the number of bins and the minimum and the maximum of the interval.'''
    
    nbins = int( nbins )
    size = float( upper - lower )/ nbins
    return [ lower + i*size for i in range(nbins) ]

def Interpolate( xs, ys, opt = 'float' ):
    ''' This function takes two lists and returs the function that passes by all points obtained by interpolation at every 2 points.'''
    
    def Interpolator(x0):
        d = sorted( zip( map( lambda x: abs(x-x0), xs ), zip(xs,ys) ) )
        x1,y1 = d[0][1]
        x2,y2 = d[1][1]

        try:
            m = float(y2-y1)/(x2-x1)
        except:
            return y1
        
        n = y1 - m*x1

        if opt=='int':
            return int(m*x+n)
        return m*x0+n
    
    return Interpolator




