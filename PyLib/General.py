#
# Module with some general functions.
#
#
# Author: Gonzalo Martinez
#
# Last update: 17 / 03 / 2014
#

from time import time
from math import ceil, floor

LETTERS  = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
letters  = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
Nletters = len(letters)

letter_dictionary = {}
for i,j in zip(LETTERS,letters):
    letter_dictionary[i] = j
    letter_dictionary[j] = i

del i,j

SUM  = lambda x,y: x + y
SUBS = lambda x,y: x - y
MULT = lambda x,y: x * y
DIV  = lambda x,y: x / y

rint = lambda x: int( round( x ) )
fint = lambda x: int( floor( x ) )
cint = lambda x: int(  ceil( x ) )

def S2HMS( s ):
    h, m = 0, 0

    if s >= 3600:
        h  = s // 3600
        s -= h * 3600.
    if s >= 60:
        m  = s // 60
        s -= m * 60

    return h, m, s

def ElapsedTime( t0 = 0. ):
    ''' Returns the diffence in time since t0 in a readable way.'''

    dt = S2HMS( time() - t0 )
    return '{0} h {1} min {2} s'.format(*dt)

def Wait( message = 'Waiting...' ):
    ''' Prints a message and waits for a input.'''

    raw_input( message )

def GetVarName( var, exception = None ):
    ''' Returns the name of the variable "var". Also accepts an exception (if two variables points to the same mamory position.'''
    
    variables = globals()
    for v in variables.keys():
        if var == variables[v] and v != exception:
            return str( v )

    return None

def readdata( filename, separator = ' ', type = 'float', skip = 0):
    ''' Reads data from a file and returns a list of lists of data. If there is more than one column of data, you can specify the separator between them which is a space by default. Also, in order to convert this data from strings to numbers you can specify the type of numbers, which is taken like floats by default, but you can choose also integers.'''
    
    f = open(filename,'r')
    lines = f.readlines()
    f.close()
    
    ndata = len ( lines[0].split(separator) )
    vars=[ [] for i in range(ndata) ]
    
    for i,line in enumerate(lines):
        if i<skip:
            continue
        aux = line.split(separator)
        if type == 'float':
            map( lambda i,x: vars[i].append( float(x) ), range( len(aux) ), aux )
        elif type == 'int':
            map( lambda i,x: vars[i].append( int  (x) ), range( len(aux) ), aux )
        elif type == 'str':
            map( lambda i,x: vars[i].append( str  (x) ), range( len(aux) ), aux )

    return vars[0] if ndata is 1 else vars

def PrintVars( *Vars ):
    ''' Shows the value of a serie of variables with its names. '''
    
    if Vars == ():
        Vars = globals().values()
    
    for v in Vars:
        print GetVarName(v) + ' = ' + str(v)



