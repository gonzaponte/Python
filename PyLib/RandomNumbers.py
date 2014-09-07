#
# Module with random numbers generators.
#
#
# Author: Gonzalo Martinez
#
# Last update: 17 / 03 / 2014
#

from ROOT import TRandom3
from General import rint

class RandomChoice:
    
    def __init__( self, *P ):
        self.R = TRandom3()
        self.R.SetSeed(0)
        self.eps = 1e-20
        
        self.n = len( P )
        self.D = dict( enumerate( P ) )
    
        self.low = -0.5 + self.eps
        self.up  = self.n - 0.5 - self.eps

    def Get( self ):
        return self.D[ rint( self.R.Uniform( self.low, self.up ) ) ]


class FastRandom:
    ''' Fast, but bad random generator.'''
    
    def __init__( self, idum ):
        ''' Constructor. Initialize with a non-zero integer seed.'''
        
        self.IA   = 16807
        self.IM   = 2147483647
        self.AM   = 1.0 / self.IM
        self.IQ   = 127773
        self.IR   = 2836
        self.NTAB = 32
        self.NDIV = 1 + ( self.IM - 1 ) / self.NTAB
        self.EPS  = 1.2e-7
        self.RNMX = 1.0 - self.EPS

        self.iy   = 0L
        self.iv   = map( long, range(self.NTAB) )
        self.temp = 0.
        self.idum = - int( abs( idum ) )
        
        if not self.idum:
            raise TypeError('Error in FastRandom: Seed must be a non-zero integer.')
        
        self.__ShuffleTable()
    
    def Uniform( self ):
        ''' Returns a uniform-deviated random number between 0 and 1.'''
        
        if self.idum <= 0 or not self.iy:
            self.__ShuffleTable()
        
        k          = self.idum / self.IQ
        self.idum  = self.IA * ( self.idum - k * self.IQ ) - self.IR * k;
        self.idum += self.IM if self.idum < 0 else 0

        j          = self.iy / self.NDIV
        self.iy    = self.iv[j]
        self.iv[j] = self.idum
        self.temp  = float( self.AM * self.iy )
    
        return self.temp if not self.temp > self.RNMX else self.RNMX

    def __ShuffleTable( self ):
        ''' Generates a new table.'''
        
        self.idum  = +1 if self.idum > -1 else -self.idum
        
        for j in range( self.NTAB + 8 )[::-1]:
            
            k          = self.idum / self.IQ
            self.idum  = self.IA * ( self.idum - k * self.IQ ) - self.IR * k
            self.idum += self.IM if self.idum < 0 else 0
            
            if j < self.NTAB :
                self.iv[j] = long(self.idum);
        
        self.iy = long(self.iv[0])


class GoodRandom:
    ''' Good random number generator. It is also slower.'''
    
    def __init__( self, idum ):
        ''' Constructor. Initialize with a non-zero integer seed.'''
        
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
        self.EPS   = 1.2e-7
        self.RNMX  = 1.0 - self.EPS
        
        self.idum  = - int( abs( idum ) )
        self.idum2 = 123456789L
        self.iy    = 0L
        self.iv    = map( long, range(self.NTAB) )
        self.temp  = 0.
            
        
        if not self.idum:
            raise TypeError('Error in GoodRandom: Seed must be a non-zero integer.')
        
        self.__ShuffleTable()



    def Uniform( self ):
        ''' Returns a uniform-deviated random number between 0 and 1.'''
        
        if self.idum <= 0:
            self.__ShuffleTable()
        
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


    def __ShuffleTable( self ):
        ''' Generates a new table.'''
        
        self.idum  = 1 if self.idum > -1 else -self.idum
        self.idum2 = int( self.idum )

        for j in range( self.NTAB + 8 )[::-1]:
            
            k          = self.idum / self.IQ1
            self.idum  = self.IA1 * ( self.idum - k * self.IQ1 ) - k * self.IR1
            self.idum += self.IM1 if self.idum < 0 else 0
            
            if ( j < self.NTAB ):
                self.iv[j] = long(self.idum);

        self.iy = long(self.iv[0])

#class PerfectRandom:
#    ''' *** WORKING ON IT. DO NOT USE YET*** Very fast and long-period random number generator.'''
#
#    def __init__( self, seed ):
#        ''' Class constructor.'''
#        raise RunTimeError('*** WORKING ON PerfectRandom. DO NOT USE YET.***')
#        self.NN = 312
#        self.MM = 156
#        self.MATRIX_A = 0xB5026F5AA96619E9ULL
#        self.UM =  0xFFFFFFFF80000000ULL
#        self.LM = 0x7FFFFFFFULL
#
#        self.mt = map( long, range( self.NN ) )
#        self.mti = self.NN + 1
#
#        self.mt[0] = int(seed)
#        for i in xrange( 1, self.NN ):
#            mt[i] = (6364136223846793005ULL * (mt[mti-1] ^ (mt[mti-1] >> 62)) + mti);
#
#/* initializes mt[NN] with a seed */
#void init_genrand64(unsigned long long seed)
#{
#    mt[0] = seed;
#    for (mti=1; mti<NN; mti++)
#        mt[mti] =  (6364136223846793005ULL * (mt[mti-1] ^ (mt[mti-1] >> 62)) + mti);
#}
#
#/* initialize by an array with array-length */
#/* init_key is the array for initializing keys */
#/* key_length is its length */
#void init_by_array64(unsigned long long init_key[],
#                     unsigned long long key_length)
#{
#    unsigned long long i, j, k;
#    init_genrand64(19650218ULL);
#    i=1; j=0;
#    k = (NN>key_length ? NN : key_length);
#    for (; k; k--) {
#        mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 62)) * 3935559000370003845ULL))
#            + init_key[j] + j; /* non linear */
#        i++; j++;
#        if (i>=NN) { mt[0] = mt[NN-1]; i=1; }
#        if (j>=key_length) j=0;
#    }
#    for (k=NN-1; k; k--) {
#        mt[i] = (mt[i] ^ ((mt[i-1] ^ (mt[i-1] >> 62)) * 2862933555777941757ULL))
#            - i; /* non linear */
#        i++;
#        if (i>=NN) { mt[0] = mt[NN-1]; i=1; }
#    }
#    
#    mt[0] = 1ULL << 63; /* MSB is 1; assuring non-zero initial array */
#}
#
#/* generates a random number on [0, 2^64-1]-interval */
#unsigned long long genrand64_int64(void)
#{
#    int i;
#    unsigned long long x;
#    static unsigned long long mag01[2]={0ULL, MATRIX_A};
#    
#    if (mti >= NN) { /* generate NN words at one time */
#        
#        /* if init_genrand64() has not been called, */
#        /* a default initial seed is used     */
#        if (mti == NN+1)
#            init_genrand64(5489ULL);
#        
#        for (i=0;i<NN-MM;i++) {
#            x = (mt[i]&UM)|(mt[i+1]&LM);
#            mt[i] = mt[i+MM] ^ (x>>1) ^ mag01[(int)(x&1ULL)];
#        }
#        for (;i<NN-1;i++) {
#            x = (mt[i]&UM)|(mt[i+1]&LM);
#            mt[i] = mt[i+(MM-NN)] ^ (x>>1) ^ mag01[(int)(x&1ULL)];
#        }
#        x = (mt[NN-1]&UM)|(mt[0]&LM);
#        mt[NN-1] = mt[MM-1] ^ (x>>1) ^ mag01[(int)(x&1ULL)];
#        
#        mti = 0;
#    }
#    
#    x = mt[mti++];
#    
#    x ^= (x >> 29) & 0x5555555555555555ULL;
#    x ^= (x << 17) & 0x71D67FFFEDA60000ULL;
#    x ^= (x << 37) & 0xFFF7EEE000000000ULL;
#    x ^= (x >> 43);
#    
#    return x;
#}
#
#/* generates a random number on [0, 2^63-1]-interval */
#long long genrand64_int63(void)
#{
#    return (long long)(genrand64_int64() >> 1);
#}
#
#/* generates a random number on [0,1]-real-interval */
#double genrand64_real1(void)
#{
#    return (genrand64_int64() >> 11) * (1.0/9007199254740991.0);
#}
#
#/* generates a random number on [0,1)-real-interval */
#                                 double genrand64_real2(void)
#                                 {
#                                 return (genrand64_int64() >> 11) * (1.0/9007199254740992.0);
#                                 }
#                                 
#                                 /* generates a random number on (0,1)-real-interval */
#                                 double genrand64_real3(void)
#                                 {
#                                 return ((genrand64_int64() >> 12) + 0.5) * (1.0/4503599627370496.0);
#                                 }
#                                 
#                                 
#                                 int main(void)
#                                 {
#                                 int i;
#                                 unsigned long long init[4]={0x12345ULL, 0x23456ULL, 0x34567ULL, 0x45678ULL}, length=4;
#                                 init_by_array64(init, length);
#                                 printf("1000 outputs of genrand64_int64()\n");
#                                 for (i=0; i<1000; i++) {
#                                 printf("%20llu ", genrand64_int64());
#                                 if (i%5==4) printf("\n");
#                                 }
#                                 printf("\n1000 outputs of genrand64_real2()\n");
#                                 for (i=0; i<1000; i++) {
#                                 printf("%10.8f ", genrand64_real2());
#                                 if (i%5==4) printf("\n");
#                                 }
#                                 return 0;
#                                 }
