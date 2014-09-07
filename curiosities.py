import sys
from math import *
from check import *

def sqroot( x, p=1e-20 ):
    ''' This function takes any real number and performs the square root by the Newton method. Optionally you can set the precision of the solution with another argument.'''
    
    if not isreal(x):
        wrong(sqroot)
    
    b = float(x)
    dif = float('inf')
    while dif > p:
        a = b
        b = 0.5 * ( x/a + a )
        dif = abs( b - a )
    return a

def fibo( N ):
    ''' This function takes an integer N and returns a list with the first N numbers of the Fibbonacci serie.'''
    
    if not isint(N) or N<2:
        wrong(fibo)
    
    if N==1:
        return [0]
    #If N is 1 the rest of the function is not executed
    n1 = 0
    n2 = 1
    list = [ n1, n2 ]
    for i in range(N-2):
        n3 = n1 + n2
        list += [n3]
        n1 = n2
        n2 = n3
    return list

def isprime( N ):
    ''' This function verifies if a number is prime.'''
    
    if not isint(N) or N<0:
        wrong(isprime)
    
    d = divisors(N)
    if len(d)==2:
        return True
    return False

def iseven( N ):
    ''' This function verifies if a number is even.'''
    
    if not isint(N):
        wrong(iseven)

    if N%2:
        return False
    return True

def Fermat( a,b,n=100 ):
    ''' This function checks the fermats theorem.'''
    for i in range(3,n):
        ci = a**i + b**i
        c = ci**(1./i)
        if not c-round(c):
            if round(c)**n == ci:
                print 'It is false'
                return False
    print 'It is true up to order n=',n
    return True

def divisors( N ):
    ''' This function returns a list with the divisors of the argument.'''
    
    if not isint(N):
        wrong(divisors)

    if iseven(N):
        r = range( 1, N/2 +1)
    else:
        r = range( 1, N/2 + 2 )

    return filter( lambda x: not N%x, r ) + [N]

def MCD(a,b):
    ''' This function takes two real numbers and returns their maximum common divisor.'''
    if b>a:
        temp = b
        b=a
        a=temp
    if not b:
        return a
    return MCD( b, a%b )


def order( list, number=0 ):
    ''' This function orders a list by its distance to a given number.'''
    d = zip( map( lambda x: abs(x-number), list ), list )
    d.sort()
    return zip(*d)[1]

#def nlines( file ):
#    f = open( file, 'r' )
#    return len(f.readlines())

def nlines( string ):
    ''' This function counts the number of lines in a string.'''
    return len( filter( lambda x: x=='\n', string ) )

#def nwords( file ):
#    f = open( file, 'r' )
#    lines = f.readlines()
#    n = 0
#    for line in lines:
#        n += len( line.split() )
#    return n

def nwords( string ):
    ''' This function counts the number of words in a string. It is supposed that after each end of line there is a space.'''
    return len( filter( lambda x: x==' ', string ) )

#def nupper( file ):
#    f = open( file, 'r' )
#    lines = f.readlines()
#    n=0
#    for line in lines:
#        for l in line:
#            if l.isupper():
#                n += 1
#    return n

def nupper( string ):
    ''' This function counts the number of upper letters in a string.'''
    return len( filter( lambda x: x.isupper(), string ) )

def palindrome( string ):
    ''' This function checks if a string is a palindrome.'''
    string=string.replace(' ','',string.count(' '))
    for i in range( len(string)/2 ):
        if not string[i]==string[-i-1]:
            return False
    return True

def power2(N):
    n=0
    while not N==1:
        if N%2:
            return False
        else:
            n += 1
            N /= 2
    return n

def polinomial(ai):
    def pol(x):
        p=0
        for i in range(len(ai)):
            p += ai[i]*x**i
        return p
    return pol

def cumulative( fun, n0=0 ):
    ''' This function calculates the integral of a discrete function. It takes the function and the starting point and returns the cdf.'''
    
    return lambda nn: sum( map( fun, range(n0, nn+1) ) )

def integral( fun, x0=0, size=0.01 ):
#    def riemann( xn ):
#        I = 0
#        l = (xn - x0)/float(size)
#        i=0
#        while i<l:
#            I += fun( x0 + (i+0.5)*size )
#            i += 1
#        I *= size
#        return I
    return lambda xn: sum( map( fun, binning((xn - x0)/float(size),x0,xn)) )*size

def cdf( pdf, min=0, opt='float' ):
    if opt=='float':
        return integral( pdf, min )
    elif opt=='int':
        return cumulative( pdf, min )
    else:
        wrong(pdf2cdf)

def Ptotal( cdf, min=0, max = 1, percent=0.9, opt='float' ):
    if opt=='float':
        i=min
        step = (max - min)*0.001
        while i<=max:
            if cdf(i)>=percent:
                return i
            i += step
        print 'The cdf does not reach this percentage in that range'
        return -1
    elif opt=='int':
        i=min
        while i<=max:
            if cdf(i)>=percent:
                return i
            i += 1
        print 'The cdf does not reach this percentage in that range'
        return -1

def stat(pdf,min=0,max=1e5,opt='float'):
    if opt=='int':
        x = range(min,max)
    else:
        x = binning(1000*(max-min),min,max)
    
    return statistics( x, map( lambda y: 1/sqrt(y+1e-8), map(pdf, x) ) )


def invcdf(pdf,lower=0,upper=1,opt='float'):
    cum = cdf( pdf, lower, opt)
    p = 1e-5
    def inv(x):
        min=lower
        max=upper
        dif = p
        while abs(dif)>=p:
            dif = cum( (max + min)/2. ) - x
            if dif>0:
                max = (max + min)/2.
            elif dif<0:
                min = (max + min)/2.
        return (max + min)/2.
    return inv


def makedic( list1, list2 ):
    ''' This function takes 2 containers and returns a dictionary which keys are the elements of the first argument and the values are the elements of the second argument assigned one by one. In the case they are dictionaries, the function takes their keys as arguments.'''
    
    if not iscontainer(list1) or not iscontainer(list2):
        wrong(makedic)
    if not lengths( list1, list2 ):
        sys.exit( 'Error in makedic: the arguments must have the same size' )
    
    return dict( zip(list1,list2) )

def invertdic( dic ):
    ''' This function takes a dictionary and returns another one which exchange values and keys of the former one.'''
    
    if not isdic(dic):
        wrong(invertdic)
    
    k,v=zip(*dic.items())
    return dict(zip(v,k))

def printdic( dic ):
    ''' This method prints a dictionary and prints its pairs key - value sorted.'''
    
    keys = dic.keys()
    keys.sort()
    for key in keys:
        print key, dic[key]



