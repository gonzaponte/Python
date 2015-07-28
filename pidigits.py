'''
    Calculation of the pi digits.
'''

def Enumerator( N0 ):
    N = N0
    while True:
        yield N
        N += 1

def A( N, k, a ):
    return pow( 16, N-k, 8 * k + a ) / float( 8. * k + a )

def B( N, k, a ):
    return pow( 16, N-k ) / float( 8. * k + a )

def Asum( N, a ):
    return sum( A( N, k, a ) for k in xrange(N-1,-1,-1) )

def Bsum( N, a, p = 16 ):
    p += 10
    return sum( B( N, k, a ) for k in xrange(N+p,N-1,-1) )
#    Sum = 0.
#    for k in Enumerator(N):
#        new  = B( N, k, p )
#        Sum += new
#        if not new:
#            return Sum

def ABsum( N, a, p = 16 ):
    return Asum( N, a ) + Bsum( N, a, p )

def Nthpi( N ):
    return str( int( str( int( 4 * ABsum( N, 1 ) - 2 * ABsum( N, 4 ) - ABsum( N, 5 ) - ABsum( N, 6 ) ) ), 16 ) )

def pi( N = 100 ):
    return ''.join( map( Nthpi, range(N) ) )

print pi()


