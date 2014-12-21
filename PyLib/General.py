#
# Module with some general functions.
#
#
# Author: Gonzalo Martinez
#
# Last update: 17 / 03 / 2014
#

import time
import math

LETTERS  = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
letters  = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
Nletters = len(letters)

letter_dictionary = {}
for i,j in zip(LETTERS,letters):
    letter_dictionary[i] = j
    letter_dictionary[j] = i

del i,j

rint = lambda x: int(      round( x ) )
fint = lambda x: int( math.floor( x ) )
cint = lambda x: int( math. ceil( x ) )

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

def readdata( filename, separator = ' ', type = float, skip = 0):
    ''' Reads data from a file and returns a list of lists of data. If there is more than one column of data, you can specify the separator between them which is a space by default. Also, in order to convert this data from strings to numbers you can specify the type of numbers, which is taken like floats by default, but you can choose also integers.'''
    
    f = open(filename,'r')
    lines = f.readlines()
    f.close()
    
    ndata = len ( lines[skip].split(separator) )
    vars=[ [] for i in range(ndata) ]
    
    if not isinstance(type,(list,tuple)):
        types = [type] * ndata

    for i,line in enumerate(lines):
        if i<skip:
            continue
        aux = line.split(separator)
        try:
            map( lambda i,x: vars[i].append( types[i](x) ), range( len(aux) ), aux )
        except:
            raise ValueError('Error reading line {0}:\n{1}'.format(i,line) )
    return vars[0] if ndata is 1 else vars

def PrintVars( *Vars ):
    ''' Shows the value of a serie of variables with its names. '''
    
    if Vars == ():
        Vars = globals().values()
    
    for v in Vars:
        print GetVarName(v) + ' = ' + str(v)



