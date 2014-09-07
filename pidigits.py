'''
    Calculation of the pi digits.
'''

def Enumerator( N0 ):
    N = N0 - 1
    while True:
        N += 1
        yield N

def A( N, k, p ):
    return pow( 16, N-k, 8 * k + p ) / float( 8 * k + p )

def B( N, k, p ):
    return pow( 16, N-k ) / float( 8 * k + p )

def Asum( N, p ):
    return sum( [ A( N, k, p ) for k in xrange(N) ] )

def Bsum( N, p ):
    Sum = 0.
    for k in Enumerator(N):
        new  = B( N, k, p )
        Sum += new
        if not new:
            return Sum

def ABsum( N, p ):
    return Asum( N, p ) + Bsum( N, p )

def Nthpi( N ):
    return ( 4 * ABsum( N, 1 ) - 2 * ABsum( N, 4 ) - ABsum( N, 5 ) - ABsum( N, 6 ) ) % 1.0

def pi( T = 10 ):
    return ' '.join( map( str, map( Nthpi, range(10) ) ) )


print pi()


