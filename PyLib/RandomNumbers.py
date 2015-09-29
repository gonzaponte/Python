#
# Module with random numbers generators.
#
#
# Author: Gonzalo Martinez
#
# Last update: 17 / 03 / 2014
#

import General
import time
import Math
import math
import Array
#from Statistics import Mean

class RandomNumberGenerator:
    '''
        Base class for random number generation. It defines the general algorithms that any generator must have.
    '''
    def __init__( self, seed = None ):
        self.seed = self.DefaultSeed() if seed is None else seed
        self._poisson_pdf  = lambda k,mean: math.pow( mean, k ) * math.exp( - mean ) / Math.Factorial( k )
        self._poisson_cdf  = lambda x,mean: Math.gamma( int( x + 1 ), mean ) / Math.Factorial( int(x) )
    
    def DefaultSeed( self ):
        '''
            Establishes a default seed based on current time.
        '''
        return int( time.time() )
    
    def Get(self):
        '''
            Returns a random number uniformily distributed in the interval [0,1). To be implemented in each particular generator.
        '''
        return 0.

    def Uniform( self, x0 = 0., x1 = 1.):
        '''
            Returns a random number uniformily distributed in the interval [x0,x1).
        '''
        return x0 + self.Get() * ( x1 - x0 )
    
    def Integer( self, x0 = 0, x1 = 100 ):
        '''
            Returns a random integer in the interval [x0,x1) == [x0,x1-1].
        '''
        return int( self.Uniform( x0, x1 ) )

    def Choose( self, items ):
        '''
            Returns a randomly-chosen element in the list items.
        '''
        return items[ self.Integer(0,len(items)) ]

    def Shuffle( self, items ):
        '''
            Returns the input list shuffled.
        '''
        copy = list(items)
        return [ copy.pop( self.Integer(0,i) ) for i in reversed(range(1,len(items)+1)) ]

    def List( self, N, kind = 'Uniform', **kwargs ):
        '''
            Returns a list of N random numbers generated according to kind. Needed arguments must be given as keyword arguments.
        '''
        exec( 'generator = self.{0}'.format(kind) )
        return [ generator( **kwargs ) for i in xrange(N) ]

    def Poisson( self, mean ):
        '''
            Return a random number according to a poisson distribution of mean mean.
        '''
        rand       = self.Get()
        i          = 0
        cumulative = 0.
        while cumulative < rand:
            cumulative = self._poisson_cdf(i,mean)
            i += 1

        return i - 1
    
    def Gauss( self, mean = 0., sigma = 1. ):
        '''
            Return a random number according to a normal distribution with mean mean and std deviation sigma.
        '''
        return mean + math.sqrt( - 2 * math.log( self.Get() ) ) * sigma * math.cos( 2 * math.pi * self.Get() )

    def Binomial( self, N, p ):
        '''
            Return a random number according to a binomial distribution of N experiments with probability of success p.
        '''
        n = 0
        for i in xrange(N+1):
            if self.Get() > p:
                continue
            n += 1
        
        return n

    def Expo( self, rate = 1. ):
        '''
            Return a random number according to an exponential distribution with rate rate.
        '''
        return - rate * math.log( self.Get() )

    def Triangular( self, x0 = 0., x1 = 1., mid = 0.5 ):
        '''
            Return a random number according to a triangular distribution from x0 to x1 with mode at mid.
        '''
        rand = self.Get()
        return x0 + math.sqrt( rand * (x1-x0)*(mid-x0) ) if rand < (mid-x0)/(x1-x0) else x1 - math.sqrt( (1-rand) * (x1-x0) * (x1-mid) )
    
    def Correlated( self, functions, CovarianceMatrix ):
        '''
            Return a list of corralated random numbers according to the CovarianceMatrix and using kind as generator. Needed arguments must be given as keyword arguments.
        '''
        return _CorrelatedRandomNumbers( functions, CovarianceMatrix )

    def SamplePDF( self, pdf, x0, x1 ):
        '''
            Sample the given function in the interval [x0,x1) using Metropolis MC.
        '''
        return _Metropolis( pdf, x0, x1, None, self )

class LCG(RandomNumberGenerator):
    '''
        Linear congruent pseudo-random number generator.
    '''
    def __init__( self, seed = None, a = 1664525, c = 1013904223, m = 4294967296 ):
        '''
            Initialize with some seed and parameters
            a --> multiplier
            c --> increment
            m --> modulus
            
            Default values for a, c and m are those suggested by Numerical Recipes and seed is given by system time.
        '''
        RandomNumberGenerator.__init__( self, seed )
        assert 0 < self.seed < m, ValueError('Seed must be smaller than m')
        self.x    = self.seed
        self.a    = int(a)
        self.c    = int(c)
        self.m    = int(m)
        self.fm   = float(m)

    def Get( self ):
        '''
            Get a pseudo-random number within the interval [0,1).
        '''
        self.x = (self.a * self. x + self.c) % self.m
        return self.x / self.fm

class MCG(LCG):
    '''
        Multiplicative congruent pseudo-random number generator.
    '''
    def __init__( self, seed = None, a = 48271, m = 2147483647 ):
        '''
            Initialize with some seed and parameters
            a --> multiplier
            m --> modulus
            
            Default values for a and m are those used in C++11's minstd_rand and seed is given by system time.
        '''
        LCG.__init__( self, seed, a, 0, m )
    
    def Get( self ):
        '''
            Get a pseudo-random number within the interval [0,1).
        '''
        self.x = (self.a * self. x) % self.m
        return self.x / self.fm

class MidSquare(RandomNumberGenerator):
    '''
        Pseudo-random number generator using mid-square method.
    '''
    def __init__( self, seed ):
        '''
            Initialize with a non-zero and non-one seed.
        '''
        RandomNumberGenerator.__init__( self, seed )
        assert seed and seed-1,ValueError('Seed must be not be zero nor one')
        self.seed = seed
        self.x    = seed

    def Get( self ):
        '''
            Get a pseudo-random number within the interval [0,1).
        '''
        self.x **= 2
        self.strx = str(self.x)
        l = len(self.strx)
        if  l % 2:
            l += 1
            self.strx = self.strx.zfill( l )
        
        self.x = int( self.strx[ l//2-2:l//2+2] )
        return self.x

class MersenneTwister(RandomNumberGenerator):
    '''
        Random number generator based on the Marsenne algorithm.
    '''
    def __init__( self, seed = None ):
        '''
            Initialize with some seed.
        '''
        RandomNumberGenerator.__init__( self, seed )
        self.index = 0
        self.MT    = []
        self._GenerateFirstTable()

    def Get( self ):
        '''
            Get a pseudo-random number within the interval [0,1).
        '''
        if self.index is 0:
            self._RegenerateTable()

        y  = self.MT[self.index]
        y ^=   y >> 11
        y ^= ( y << 7  ) & 0x9d2c5680
        y ^= ( y << 15 ) & 0xefc60000
        y ^=   y >> 18
        
        self.index = ( self.index + 1 ) % 624
        return y / (2.**32-1)

    def _GenerateFirstTable( self ):
        '''
            Generate the state vector.
        '''
        self.MT.append( self.seed )
        for i in range(1,624):
            number = 0x6c078965 * ( self.MT[-1] ^ ( self.MT[-1] >> 30 ) ) + i
            self.MT.append( number & 0xffffffff )

    def _RegenerateTable( self ):
        '''
            Generate a new table.
        '''
        for i in range(624):
            y = ( self.MT[i] & 0x80000000 ) + ( self.MT[ (i+1) % 624 ] & 0x7fffffff )
            self.MT[i] = self.MT[ (i+397) % 624 ] ^ ( y >> 1 )
            if y % 2:
                self.MT[i] ^= 0x9908b0df

class ParkMiller(RandomNumberGenerator):
    '''
        A pseudo random number generator based on the algorithm created by Park and Miller. It is fast, but bad random generator.
    '''
    
    def __init__( self, seed = None ):
        '''
            Initialize with a non-zero integer seed.
        '''
        RandomNumberGenerator.__init__( self, seed )
        self.IA   = 16807
        self.IM   = 2147483647
        self.AM   = 1.0 / self.IM
        self.IQ   = 127773
        self.IR   = 2836
        self.NTAB = 32
        self.NDIV = 1 + ( self.IM - 1 ) / self.NTAB
        self.EPS  = 1.e-15
        self.RNMX = 1.0 - self.EPS

        self.iy   = 0L
        self.iv   = map( long, range(self.NTAB) )
        self.temp = 0.
        self.idum = - int( abs( self.seed ) )
        
        assert self.idum,TypeError('Error in ParkMiller: Seed must be a non-zero integer.')
        
        self._ShuffleTable()
    
    def Get( self ):
        '''
            Get a pseudo-random number within the interval [0,1).
        '''
        if self.idum <= 0 or not self.iy:
            self._ShuffleTable()
        
        k          = self.idum / self.IQ
        self.idum  = self.IA * ( self.idum - k * self.IQ ) - self.IR * k;
        self.idum += self.IM if self.idum < 0 else 0

        j          = self.iy / self.NDIV
        self.iy    = self.iv[j]
        self.iv[j] = self.idum
        self.temp  = float( self.AM * self.iy )
    
        return self.temp if not self.temp > self.RNMX else self.RNMX

    def _ShuffleTable( self ):
        '''
            Generate a new table.
        '''
        
        self.idum  = +1 if self.idum > -1 else -self.idum
        
        for j in range( self.NTAB + 8 )[::-1]:
            
            k          = self.idum / self.IQ
            self.idum  = self.IA * ( self.idum - k * self.IQ ) - self.IR * k
            self.idum += self.IM if self.idum < 0 else 0
            
            if j < self.NTAB :
                self.iv[j] = long(self.idum);
        
        self.iy = long(self.iv[0])


class LEcuyer(RandomNumberGenerator):
    '''
        A pseudo random number generator based on the algorithm created by L'Ecuyer. It is slower than Park Miller, but more reliable.
    '''
    
    def __init__( self, seed = None ):
        '''
            Initialize with a non-zero integer seed.
        '''

        RandomNumberGenerator.__init__( self, seed )
        self.IM1   = 2147483563
        self.IM2   = 2147483399
        self.AM    = 1.0 / self.IM1
        self.IMM1  = self.IM1 - 1
        self.IA1   = 40014
        self.IA2   = 40692
        self.IQ1   = 53668
        self.IQ2   = 52774
        self.IR1   = 12211
        self.IR2   = 3791
        self.NTAB  = 32
        self.NDIV  = 1 + self.IMM1 / self.NTAB
        self.EPS   = 1.e-15
        self.RNMX  = 1.0 - self.EPS
        
        self.idum  = - int( abs( self.seed ) )
        self.idum2 = 123456789L
        self.iy    = 0L
        self.iv    = map( long, range(self.NTAB) )
        self.temp  = 0.
            
        
        assert self.idum, TypeError('Error in LEcuyer: Seed must be a non-zero integer.')
        
        self._ShuffleTable()

    def Get( self ):
        '''
            Get a pseudo-random number within the interval [0,1).
        '''
        
        if self.idum <= 0:
            self._ShuffleTable()
        
        k           = self.idum / self.IQ1
        self.idum   = self.IA1 * ( self.idum - k * self.IQ1 ) - k * self.IR1
        self.idum  += self.IM1 if self.idum < 0 else 0
        
        k           = self.idum2 / self.IQ2
        self.idum2  = self.IA2 * ( self.idum2 - k * self.IQ2 ) - k * self.IR2;
        self.idum2 += self.IM2 if self.idum2 < 0 else 0

        j           = self.iy / self.NDIV
        self.iy     = self.iv[j] - self.idum2
        self.iv[j]  = long( self.idum )
        self.iy    += self.IMM1 if self.iy < 1 else 0

        self.temp = float( self.AM * self.iy )
        return self.temp if not self.temp > self.RNMX else self.RNMX


    def _ShuffleTable( self ):
        '''
            Generate a new table.
        '''
        
        self.idum  = 1 if self.idum > -1 else -self.idum
        self.idum2 = int( self.idum )

        for j in range( self.NTAB + 8 )[::-1]:
            
            k          = self.idum / self.IQ1
            self.idum  = self.IA1 * ( self.idum - k * self.IQ1 ) - k * self.IR1
            self.idum += self.IM1 if self.idum < 0 else 0
            
            if ( j < self.NTAB ):
                self.iv[j] = long(self.idum);

        self.iy = long(self.iv[0])

class _Metropolis:
    '''
        Class for general function sampling.
    '''
    def __init__( self, pdf, x0 = 0., x1 = 1., sigma = None, Random = MersenneTwister() ):
        '''
            Initialize with some function pdf and an interval [x0,x1).
            '''
        self.pdf = pdf
        self.low = x0
        self.upp = x1
        self.x0  = 0.5 * ( x1 - x0 )
        self.x1  = self.x0
        self.fx1 = self.pdf(self.x1)
        x = [ self.low + 0.02 * (i+0.5) * self.x0 for i in range(100) ]
        y = map( self.pdf, x )
        self.sig = 0.1 * sum(map(lambda a,b:a*b,x,y))/sum(y)  if sigma is None else sigma
        print self.sig
        self.rng = Random
    
    def __call__( self ):
        '''
            Get a sample.
        '''
        x2 = self.low - 1
        while not (self.low <= x2 <= self.upp):
            x2 = self.rng.Gauss( self.x1, self.sig ) 
        fx2 = self.pdf( x2 )
        ratio = fx2 / self.fx1
        
        if ratio >= 1 or self.rng.Get() <= ratio: ### Faster if the first part of the conditional is true since
            self.x1  = x2                         ### it is not neccesary to compute another random number.
            self.fx1 = fx2 
        
        return self.x1

class _CorrelatedRandomNumbers:
    '''
        Random number generator that takes into account dependences among variables.
    '''
    def __init__( self, Vector, CovarianceMatrix ):
        '''
            Initialize with a vector of functions that produce the random numbers.
        '''
        self.uncorrelated = Array.Vector( Vector )
        self.rot_matrix   = Array.Matrix( CovarianceMatrix ).Cholesky()
        
    def __call__( self ):
        '''
            Get a list of correlated random numbers.
        '''
        return list( self.uncorrelated.Apply( lambda x: x.__call__() ) ** self.rot_matrix )

if __name__ == '__main__':
    from ROOT import TH1F, TH2F
    from Plots import PutInCanvas
    from Statistics import Distribution
    lcg = LCG()
    mcg = MCG()
    mtg = MersenneTwister()
    pmg = ParkMiller()
    leg = LEcuyer()
    
    fun = Distribution( lambda x: 0.8 * math.exp(-4.*x) + math.exp( -0.5*( (x-.5)/0.015 )**2 ) + 0.3 * math.exp( -0.5*( (x-.55)/0.01 )**2 ), 0, 1, 1e4, normalized = False )
    pdfsample = lcg.SamplePDF( fun, 0, 1 )
    
    hlcg  = TH1F( 'lcg', 'lcg',  15,  0, 15 )
    hmcg  = TH1F( 'mcg', 'mcg',  16,  0, 16 )
    hmtg  = TH1F( 'mtg', 'mtg', 100,  0,  1 )
    hpmg  = TH1F( 'pmg', 'pmg', 100, -5,  5 )
    hleg  = TH1F( 'leg', 'leg', 100,  0,  1 )
    hmet  = TH1F( 'met', 'met', 200,  0,  1 )
    
    hlcg.SetMinimum(0); hlcg.SetLineColor(1); hlcg.SetLineWidth(2)
    hmcg.SetMinimum(0); hmcg.SetLineColor(2); hmcg.SetLineWidth(2)
    hmtg.SetMinimum(0); hmtg.SetLineColor(3); hmtg.SetLineWidth(2)
    hpmg.SetMinimum(0); hpmg.SetLineColor(1); hpmg.SetLineWidth(2)
    hleg.SetMinimum(0); hleg.SetLineColor(2); hleg.SetLineWidth(2)
    hmet.SetMinimum(0); hmet.SetLineColor(2); hmet.SetLineWidth(2)
    
    for i in range(int(1e5)):
#        hlcg.Fill( lcg.Poisson(3) )
        hmcg.Fill( mcg.Binomial(10,0.8) )
        hmtg.Fill( mtg.Triangular(0.,1.,0.2) )
        hpmg.Fill( pmg.Gauss(0.,1.) )
        hleg.Fill( leg.Expo(.2) )
        hmet.Fill( pdfsample() )

    canv = PutInCanvas( [hlcg,hmcg,hmtg,hpmg,hleg,hmet] )

    hcorr = TH2F('hcorr','hcorr',100,0,1,200,-5,5)
    alpha = -0.9
    C = [[1,alpha],[alpha,1]]
    corrg = mtg.Correlated( [ mtg.Uniform, mtg.Uniform], C )
    for i in range(10000): x = hcorr.Fill( *corrg() )
    canv2 = PutInCanvas( [hcorr], ['zcol'] )






